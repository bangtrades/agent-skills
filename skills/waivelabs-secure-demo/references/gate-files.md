# Portable gate — source files

Copy these into any Next.js 14 (App Router) client demo. Generalized from the VAIL build:
generic `WL_*` env vars, `wl_sess` cookie, and **`WL_DEMO_SCOPE` enforcement** so a code only
opens the demo it was minted for. Styling uses inline styles + optional brand CSS vars
(`--brand`, `--brand-deep`, `--ink`, `--panel`) with dark fallbacks — pass the client's brand
tokens to theme it.

Env vars (Vercel · Production): `WL_SUPA_URL`, `WL_SUPA_KEY` (publishable), `WL_SESSION_SECRET`
(`openssl rand -hex 32`), `WL_DEMO_SCOPE` (e.g. `summer-fridays`).

---

## `lib/auth/session.ts`
```ts
const enc = new TextEncoder();
function b64url(b: Uint8Array){let s='';for(let i=0;i<b.length;i++)s+=String.fromCharCode(b[i]);return btoa(s).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');}
function fromB64url(str: string){let s=str.replace(/-/g,'+').replace(/_/g,'/');while(s.length%4)s+='=';const bin=atob(s);const u=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);return u;}
async function key(secret:string){return crypto.subtle.importKey('raw',enc.encode(secret),{name:'HMAC',hash:'SHA-256'},false,['sign','verify']);}
export type Session={code:string;sid:string;label:string;org:string;demo:string;exp:number};
export async function signSession(p:Session,secret:string){const body=b64url(enc.encode(JSON.stringify(p)));const sig=await crypto.subtle.sign('HMAC',await key(secret),enc.encode(body));return body+'.'+b64url(new Uint8Array(sig));}
export async function verifySession(token:string,secret:string):Promise<Session|null>{const d=token.indexOf('.');if(d<0)return null;const body=token.slice(0,d),sig=token.slice(d+1);let ok=false;try{ok=await crypto.subtle.verify('HMAC',await key(secret),fromB64url(sig),enc.encode(body));}catch{return null;}if(!ok)return null;try{const p=JSON.parse(new TextDecoder().decode(fromB64url(body)))as Session;if(p.exp&&Date.now()>p.exp)return null;return p;}catch{return null;}}
```

## `lib/auth/supa.ts`
```ts
export async function rpc(fn: string, args: Record<string, any>): Promise<any> {
  const url = process.env.WL_SUPA_URL, apikey = process.env.WL_SUPA_KEY;
  if (!url || !apikey) return { ok: false, reason: 'not_configured' };
  try {
    const res = await fetch(`${url}/rest/v1/rpc/${fn}`, {
      method: 'POST',
      headers: { apikey, authorization: `Bearer ${apikey}`, 'content-type': 'application/json' },
      body: JSON.stringify(args), cache: 'no-store',
    });
    if (!res.ok) return { ok: false, reason: 'rpc_http_' + res.status };
    return await res.json();
  } catch { return { ok: false, reason: 'rpc_exception' }; }
}
```

## `middleware.ts`
```ts
import { NextResponse, type NextRequest } from 'next/server';
import { verifySession } from '@/lib/auth/session';
import { rpc } from '@/lib/auth/supa';
export const config = { matcher: ['/((?!_next/static|_next/image|favicon.ico|login|vadmin|api|.*\\.(?:png|jpg|jpeg|svg|gif|webp|ico|css|js|map|woff|woff2|ttf)).*)'] };
export async function middleware(req: NextRequest) {
  const secret = process.env.WL_SESSION_SECRET || '';
  const scope = process.env.WL_DEMO_SCOPE || '';
  const token = req.cookies.get('wl_sess')?.value;
  const login = new URL('/login', req.url); login.searchParams.set('next', req.nextUrl.pathname);
  const bounce = (reason: string) => { login.searchParams.set('reason', reason); const r = NextResponse.redirect(login); r.cookies.delete('wl_sess'); return r; };
  if (!token) return NextResponse.redirect(login);
  const sess = await verifySession(token, secret);
  if (!sess) return bounce('expired');
  if (scope && sess.demo && sess.demo !== scope) return bounce('invalid');   // code minted for another demo
  const chk = await rpc('vail_check', { p_code: sess.code, p_session: sess.sid });
  if (!chk || chk.ok !== true) return bounce(chk?.reason || 'revoked');
  if (scope && chk.demo && chk.demo !== scope) return bounce('invalid');
  return NextResponse.next();
}
```

## `app/api/auth/login/route.ts`
```ts
export const runtime = 'nodejs';
import { NextResponse } from 'next/server';
import { rpc } from '@/lib/auth/supa';
import { signSession } from '@/lib/auth/session';
export async function POST(req: Request) {
  let code=''; try { code=(await req.json()).code?.toString().trim().toUpperCase()||''; } catch {}
  if (!code) return NextResponse.json({ ok:false, reason:'invalid' }, { status:400 });
  const scope = process.env.WL_DEMO_SCOPE || '';
  const ip = (req.headers.get('x-forwarded-for')||'').split(',')[0].trim();
  const ua = req.headers.get('user-agent')||'';
  const sid = crypto.randomUUID();
  const r = await rpc('vail_login', { p_code:code, p_session:sid, p_ip:ip, p_ua:ua });
  if (!r || r.ok !== true) return NextResponse.json({ ok:false, reason:r?.reason||'invalid' }, { status:401 });
  if (scope && r.demo && r.demo !== scope) return NextResponse.json({ ok:false, reason:'invalid' }, { status:401 });
  const DAY=864e5; let maxAge=DAY;
  if (r.expires_at){ const left=new Date(r.expires_at).getTime()-Date.now(); if(left>0&&left<maxAge)maxAge=left; }
  const token = await signSession({ code, sid, label:r.label||'', org:r.org||'', demo:r.demo||'', exp:Date.now()+maxAge }, process.env.WL_SESSION_SECRET||'');
  const res = NextResponse.json({ ok:true, label:r.label, org:r.org });
  res.cookies.set('wl_sess', token, { httpOnly:true, secure:true, sameSite:'lax', path:'/', maxAge:Math.floor(maxAge/1000) });
  return res;
}
```

## `app/api/auth/logout/route.ts`
```ts
export const runtime = 'nodejs';
import { NextResponse } from 'next/server';
export async function POST(){ const r=NextResponse.json({ok:true}); r.cookies.delete('wl_sess'); return r; }
```

## `app/api/auth/me/route.ts`
```ts
export const runtime = 'nodejs';
import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { verifySession } from '@/lib/auth/session';
export async function GET(){
  const t=cookies().get('wl_sess')?.value;
  if(!t) return NextResponse.json({ok:false},{status:401});
  const s=await verifySession(t, process.env.WL_SESSION_SECRET||'');
  if(!s) return NextResponse.json({ok:false},{status:401});
  return NextResponse.json({ok:true,label:s.label,org:s.org});
}
```

## `app/api/vadmin/route.ts`
```ts
export const runtime = 'nodejs';
import { NextResponse } from 'next/server';
import { rpc } from '@/lib/auth/supa';
export async function POST(req: Request){
  let body:any={}; try{ body=await req.json(); }catch{}
  const { action, secret } = body;
  if(!secret) return NextResponse.json({ok:false,reason:'no_secret'},{status:401});
  const scope = process.env.WL_DEMO_SCOPE || 'vail';
  let r:any;
  switch(action){
    case 'list': r=await rpc('vail_admin_list',{p_admin:secret}); break;
    case 'create': {
      const code=(body.code||genCode(body.org)).toString().toUpperCase();
      const days=Number(body.days)||7;
      const expires=days>0?new Date(Date.now()+days*864e5).toISOString():null;
      r=await rpc('vail_admin_create',{p_admin:secret,p_code:code,p_label:body.label||'',p_org:body.org||'',p_demo:scope,p_expires_at:expires,p_note:body.note||''}); break;
    }
    case 'revoke': r=await rpc('vail_admin_revoke',{p_admin:secret,p_code:body.code}); break;
    case 'unrevoke': r=await rpc('vail_admin_unrevoke',{p_admin:secret,p_code:body.code}); break;
    case 'reset': r=await rpc('vail_admin_reset_session',{p_admin:secret,p_code:body.code}); break;
    default: return NextResponse.json({ok:false,reason:'bad_action'},{status:400});
  }
  const status=r?.ok?200:(r?.reason==='unauthorized'?401:400);
  return NextResponse.json(r,{status});
}
function genCode(org:string){const tag=(org||'GEN').replace(/[^A-Za-z]/g,'').slice(0,3).toUpperCase()||'GEN';return `WL-${tag}-${Math.floor(100000+Math.random()*900000)}`;}
```
> Note: `create` forces `p_demo = WL_DEMO_SCOPE`, and `list` shows ALL codes (the shared admin
> sees every demo's codes — fine for a solo operator). To scope the admin list per demo, filter
> client-side by `demo === scope`.

## `app/login/page.tsx`, `app/vadmin/page.tsx`, `components/Watermark.tsx`
These are UI — copy them from the reference deployment (Healthcare Context Engine):
`demo/app/login/page.tsx`, `demo/app/vadmin/page.tsx`, `demo/components/vail/Watermark.tsx`.
Generalize: change cookie/env names to `wl_*` (login posts to `/api/auth/login`; logout/me as above),
swap brand strings, and theme via the client's brand vars. Mount `<Watermark label org />` in the
authenticated shell (fetch `/api/auth/me` to get identity); render `/login` and `/vadmin` without
the app's nav chrome. The Watermark also wires `contextmenu`/`copy`/`cut`/`dragstart` preventers.

> [!warning] `app/vadmin/` NOT `app/__vadmin/` — `_`-prefixed App Router folders are private (404).
