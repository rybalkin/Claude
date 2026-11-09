# Test App

A small test web app (counter, to-do list, device check) that you can add to your Android home screen and open like an app: full screen, its own icon, works offline.

## Put it on your home screen

1. Open the app's web address in **Chrome** on your phone.
2. Tap **Add to home screen** in the app, or Chrome's **⋮** menu → **Add to home screen** / **Install app**.
3. Open it from the new **Test App** icon.

The page must be served over HTTPS (GitHub Pages, Netlify, …) for the install option to appear.

## Run locally

```bash
cd android-test-app
python3 -m http.server 8080   # http://localhost:8080
```
