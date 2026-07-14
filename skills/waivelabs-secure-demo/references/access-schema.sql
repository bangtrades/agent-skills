-- WaiveLabs shared demo access-control schema (Supabase / Postgres).
-- Provision ONCE per Supabase project; every client demo reuses it.
-- Already applied to the `waivelabs` project (ref frkfayhxtgcereutdyap).
-- Tables are RLS-locked with NO policies; all access is via SECURITY DEFINER RPCs.
-- Privileged ops require the admin secret, verified DB-side against a bcrypt hash.
-- (Functions are prefixed vail_* for historical reasons — they are demo-agnostic;
--  the `demo` column scopes each code to one demo, e.g. 'vail', 'summer-fridays'.)

create extension if not exists pgcrypto with schema extensions;

create table if not exists public.vail_admin (
  id int primary key default 1,
  secret_hash text not null,
  check (id = 1)
);

create table if not exists public.vail_access_codes (
  id uuid primary key default gen_random_uuid(),
  code text unique not null,
  label text not null default '',
  org text not null default '',
  demo text not null default 'vail',        -- scope: which demo this code may open
  note text default '',
  created_at timestamptz not null default now(),
  expires_at timestamptz,
  revoked boolean not null default false,
  bound_session text,                        -- single-session binding
  bound_at timestamptz,
  last_seen_at timestamptz,
  last_ip text,
  view_count int not null default 0
);

create table if not exists public.vail_access_events (
  id bigserial primary key,
  code text, event text, ip text, ua text,
  at timestamptz not null default now()
);

alter table public.vail_admin enable row level security;
alter table public.vail_access_codes enable row level security;
alter table public.vail_access_events enable row level security;

create or replace function public.vail_admin_ok(p_admin text)
returns boolean language sql security definer set search_path = public, extensions as $$
  select exists (select 1 from public.vail_admin where secret_hash = crypt(p_admin, secret_hash));
$$;

create or replace function public.vail_login(p_code text, p_session text, p_ip text, p_ua text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare r public.vail_access_codes;
begin
  select * into r from public.vail_access_codes where code = p_code;
  if not found then
    insert into public.vail_access_events(code,event,ip,ua) values (p_code,'login_invalid',p_ip,p_ua);
    return jsonb_build_object('ok',false,'reason','invalid'); end if;
  if r.revoked then return jsonb_build_object('ok',false,'reason','revoked'); end if;
  if r.expires_at is not null and r.expires_at < now() then return jsonb_build_object('ok',false,'reason','expired'); end if;
  if r.bound_session is not null and r.bound_session <> p_session and coalesce(r.last_ip,'') <> coalesce(p_ip,'') then
    return jsonb_build_object('ok',false,'reason','in_use'); end if;
  update public.vail_access_codes
     set bound_session = p_session, bound_at = coalesce(bound_at, now()),
         last_seen_at = now(), last_ip = p_ip, view_count = view_count + 1
   where code = p_code;
  insert into public.vail_access_events(code,event,ip,ua) values (p_code,'login_ok',p_ip,p_ua);
  return jsonb_build_object('ok',true,'label',r.label,'org',r.org,'demo',r.demo,'expires_at',r.expires_at);
end; $$;

create or replace function public.vail_check(p_code text, p_session text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare r public.vail_access_codes;
begin
  select * into r from public.vail_access_codes where code = p_code;
  if not found or r.revoked then return jsonb_build_object('ok',false,'reason','revoked'); end if;
  if r.expires_at is not null and r.expires_at < now() then return jsonb_build_object('ok',false,'reason','expired'); end if;
  if r.bound_session is not null and r.bound_session <> p_session then return jsonb_build_object('ok',false,'reason','in_use'); end if;
  update public.vail_access_codes set last_seen_at = now() where code = p_code;
  return jsonb_build_object('ok',true,'label',r.label,'org',r.org,'demo',r.demo);
end; $$;

create or replace function public.vail_admin_create(p_admin text, p_code text, p_label text, p_org text, p_demo text, p_expires_at timestamptz, p_note text)
returns jsonb language plpgsql security definer set search_path = public as $$
begin
  if not public.vail_admin_ok(p_admin) then return jsonb_build_object('ok',false,'reason','unauthorized'); end if;
  insert into public.vail_access_codes(code,label,org,demo,expires_at,note)
    values (p_code, coalesce(p_label,''), coalesce(p_org,''), coalesce(p_demo,'vail'), p_expires_at, coalesce(p_note,''));
  return jsonb_build_object('ok',true,'code',p_code);
exception when unique_violation then return jsonb_build_object('ok',false,'reason','exists');
end; $$;

create or replace function public.vail_admin_revoke(p_admin text, p_code text)
returns jsonb language plpgsql security definer set search_path = public as $$
begin
  if not public.vail_admin_ok(p_admin) then return jsonb_build_object('ok',false,'reason','unauthorized'); end if;
  update public.vail_access_codes set revoked = true where code = p_code;
  insert into public.vail_access_events(code,event) values (p_code,'revoked');
  return jsonb_build_object('ok',true);
end; $$;

create or replace function public.vail_admin_unrevoke(p_admin text, p_code text)
returns jsonb language plpgsql security definer set search_path = public as $$
begin
  if not public.vail_admin_ok(p_admin) then return jsonb_build_object('ok',false,'reason','unauthorized'); end if;
  update public.vail_access_codes set revoked = false where code = p_code;
  return jsonb_build_object('ok',true);
end; $$;

create or replace function public.vail_admin_reset_session(p_admin text, p_code text)
returns jsonb language plpgsql security definer set search_path = public as $$
begin
  if not public.vail_admin_ok(p_admin) then return jsonb_build_object('ok',false,'reason','unauthorized'); end if;
  update public.vail_access_codes set bound_session = null, bound_at = null where code = p_code;
  insert into public.vail_access_events(code,event) values (p_code,'session_reset');
  return jsonb_build_object('ok',true);
end; $$;

create or replace function public.vail_admin_list(p_admin text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare result jsonb;
begin
  if not public.vail_admin_ok(p_admin) then return jsonb_build_object('ok',false,'reason','unauthorized'); end if;
  select coalesce(jsonb_agg(to_jsonb(c) order by c.created_at desc), '[]'::jsonb) into result from public.vail_access_codes c;
  return jsonb_build_object('ok',true,'codes',result);
end; $$;

grant execute on function public.vail_login(text,text,text,text) to anon, authenticated;
grant execute on function public.vail_check(text,text) to anon, authenticated;
grant execute on function public.vail_admin_create(text,text,text,text,text,timestamptz,text) to anon, authenticated;
grant execute on function public.vail_admin_revoke(text,text) to anon, authenticated;
grant execute on function public.vail_admin_unrevoke(text,text) to anon, authenticated;
grant execute on function public.vail_admin_reset_session(text,text) to anon, authenticated;
grant execute on function public.vail_admin_list(text) to anon, authenticated;
grant execute on function public.vail_admin_ok(text) to anon, authenticated;

-- Set / rotate the admin secret (run separately; not stored as a migration):
--   insert into public.vail_admin(id, secret_hash)
--   values (1, crypt('YOUR-ADMIN-SECRET', gen_salt('bf')))
--   on conflict (id) do update set secret_hash = excluded.secret_hash;

-- ── Additions (owner/persistent codes + usage analytics) ──────────────────────
alter table public.vail_access_codes add column if not exists unbound boolean not null default false;
-- vail_login / vail_check above must include the `unbound` branch:
--   login: skip the in_use check when r.unbound; set bound_session = null when r.unbound.
--   check: skip the bound_session match when r.unbound.
-- (See the reference deployment for the unbound-aware bodies.)

create or replace function public.vail_admin_events(p_admin text, p_limit int)
returns jsonb language plpgsql security definer set search_path = public as $$
declare result jsonb;
begin
  if not public.vail_admin_ok(p_admin) then return jsonb_build_object('ok',false,'reason','unauthorized'); end if;
  select coalesce(jsonb_agg(to_jsonb(e) order by e.at desc), '[]'::jsonb) into result
    from (select * from public.vail_access_events order by at desc limit coalesce(p_limit,200)) e;
  return jsonb_build_object('ok',true,'events',result);
end; $$;

create or replace function public.vail_admin_create2(p_admin text, p_code text, p_label text, p_org text, p_demo text, p_expires_at timestamptz, p_note text, p_unbound boolean)
returns jsonb language plpgsql security definer set search_path = public as $$
begin
  if not public.vail_admin_ok(p_admin) then return jsonb_build_object('ok',false,'reason','unauthorized'); end if;
  insert into public.vail_access_codes(code,label,org,demo,expires_at,note,unbound)
    values (p_code, coalesce(p_label,''), coalesce(p_org,''), coalesce(p_demo,'vail'), p_expires_at, coalesce(p_note,''), coalesce(p_unbound,false));
  return jsonb_build_object('ok',true,'code',p_code);
exception when unique_violation then return jsonb_build_object('ok',false,'reason','exists');
end; $$;

grant execute on function public.vail_admin_events(text,int) to anon, authenticated;
grant execute on function public.vail_admin_create2(text,text,text,text,text,timestamptz,text,boolean) to anon, authenticated;
