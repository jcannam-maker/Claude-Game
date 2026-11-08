# DCF Company Valuation Calculator

A 10-year discounted cash flow (DCF) calculator. It reproduces
`2026.04.25_Korvest_DCF Company Valuation Calculator.pdf` exactly and opens with
the Korvest figures from that PDF: intrinsic value $16.25 and margin-of-safety
value $13.00. It runs offline and stores saved valuations on the device.

## Model

| Step | Formula |
|---|---|
| Cash flow, years 1–10 | previous cash flow × (1 + growth for that year) |
| Present value | cash flow ÷ (1 + discount rate)^year |
| Terminal year | year-10 cash flow × (1 + terminal growth) |
| Terminal value (PV) | terminal year ÷ (discount rate − terminal growth) ÷ (1 + discount rate)^10 |
| Total PV | Σ PV of years 1–10 + terminal value |
| Intrinsic value | (total PV + net cash − net debt) ÷ shares |
| Margin-of-safety IV | IV × (1 − margin of safety) |

## iPad (installs as a home-screen app and works offline)

1. Host the app once, for free with GitHub Pages: in the repository on GitHub, go to
   **Settings → Pages**, set **Source: Deploy from a branch**, choose the branch
   that holds this folder with **/ (root)**, then click **Save**.
2. After a minute or two, open
   `https://jcannam-maker.github.io/Claude-Game/dcf-calculator/` in **Safari** on the iPad.
3. Tap **Share → Add to Home Screen → Add**.

It now opens full screen from its own icon, like any other app, and works
without an internet connection.

## Mac

**Option A: double-click app (works offline, no hosting needed)**
1. Download `dist/DCF-Valuation-mac.zip` and double-click it to unzip.
2. Drag **DCF Valuation.app** into **Applications**.
3. On first launch macOS warns that the app is from an unidentified developer,
   because it is not signed with a paid Apple certificate. Open it once with
   **right-click → Open**. On macOS 15 (Sequoia) or later, try to open it,
   then go to **System Settings → Privacy & Security** and click **Open Anyway**.
   After that it opens normally.

The app opens the calculator in your default browser.

**Option B: Dock app in its own window (macOS 14 Sonoma or later)**
Open the GitHub Pages address above in Safari, then choose **File → Add to Dock**.

## Rebuilding the Mac app after changes

```
python3 tools/build_mac_app.py      # writes dist/DCF-Valuation-mac.zip
```
