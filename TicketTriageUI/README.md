# Ticket Triage Assistant — React

React + Vite port of the original Streamlit frontend. Same pages, same
Cognito login, same backend API — just a different UI layer.

## Pages

- Login (AWS Cognito `USER_PASSWORD_AUTH`)
- Home (role-based landing page for `CUSTOMER` / `SUPPORT` groups)
- Create Ticket, My Tickets, Ticket Details (customer)
- Support Dashboard, Orders Dashboard, Approval Dashboard (support)

## Setup

1. Install [Node.js](https://nodejs.org/) 18+ (includes npm).
2. Install dependencies:

   ```
   npm install
   ```

3. Copy `.env.example` to `.env` and adjust if your API/Cognito settings differ:

   ```
   cp .env.example .env
   ```

4. Start the dev server:

   ```
   npm run dev
   ```

   Then open the URL it prints (default `http://localhost:5173`).

## Build for production

```
npm run build
```

Output goes to `dist/` — deploy it to any static host (S3 + CloudFront,
Netlify, Vercel, Amplify Hosting, etc.).

## Notes

- Auth calls Cognito's `InitiateAuth` directly from the browser using the
  same `CLIENT_ID` and `USER_PASSWORD_AUTH` flow as the Python app — no
  client secret is required, so nothing sensitive is exposed by doing this
  client-side.
- The ID token is decoded client-side (signature not verified) purely to
  read the `cognito:groups` claim, mirroring the original
  `verify_signature: False` behavior. This is fine because the API itself
  is the actual authority for any protected action.
- Session (`loggedIn`, `email`, `group`, etc.) is kept in `sessionStorage`,
  so a page refresh doesn't log you out, but closing the tab does.
