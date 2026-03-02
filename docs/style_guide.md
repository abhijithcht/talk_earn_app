# 🎨 Talk & Earn — Style Guidelines & UI/UX Review

This document serves as the central reference for the **Talk & Earn** web application design system. It details the current visual language, UI components, and provides actionable recommendations for UI/UX improvements and bug fixes.

---

## 1. Current Design System

### 1.1 Color Palette
The application uses a modern, space-themed "dark mode" aesthetic driven by CSS variables.

| Role           | CSS Variable   | Hex       | Description                                                                      |
| :------------- | :------------- | :-------- | :------------------------------------------------------------------------------- |
| **Background** | `--bg-deep`    | `#050b14` | Very dark navy/black, used as the base app background.                           |
| **Primary**    | `--primary`    | `#4f46e5` | Indigo. Used for primary actions, branding, and gradients.                       |
| **Secondary**  | `--secondary`  | `#0ea5e9` | Sky Blue. Used alongside primary for hover states and gradients.                 |
| **Accent**     | `--accent`     | `#10b981` | Emerald Green. Used for success states, earning indicators, and active statuses. |
| **Text Main**  | `--text-main`  | `#f8fafc` | Off-white. Used for primary headings and body paragraphs.                        |
| **Text Muted** | `--text-muted` | `#94a3b8` | Slate gray. Used for secondary labels, hints, and subtitles.                     |

*Gradients*: `--gradient-text` (`linear-gradient(135deg, #38bdf8, #818cf8, #c084fc)`) is used for standout headings to create a premium feel.

### 1.2 Typography
- **Font Family**: Google Fonts `Outfit` (`wght@300;400;500;600;700;800`).
- **Hierarchy**:
  - `h1-h3` use `font-weight: 700` for bold, impactful headers.
  - Body text uses `font-weight: 400`.
  - Buttons and labels use `font-weight: 500` or `600`.

### 1.3 Glassmorphism UI
The defining UI pattern is the "Glass Panel", achieved via `rgba()` backgrounds matching the deep navy tone, combined with `backdrop-filter: blur()`.

- **Background**: `rgba(16, 25, 43, 0.45)`
- **Blur**: `backdrop-filter: blur(20px)`
- **Border**: `rgba(255, 255, 255, 0.08)` (Subtle 8% white line to define the edge)
- **Shadow**: `0 8px 32px 0 rgba(0, 0, 0, 0.37)` (Deep shadow for elevation)

### 1.4 Components
- **Buttons (`.btn`)**: Pill-shaped (`border-radius: 999px`) with gradient backgrounds. They feature a hover transition that slightly translates them up (`transform: translateY(-2px)`) alongside an inner gradient overlay for a glowing effect.
- **Inputs**: Darkened backgrounds (`rgba(0, 0, 0, 0.2)`) with a thick colored outline (`box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1)`) on focus.

---

## 2. UI/UX Review: Suggested Updates & Bugfixes

While the current foundation is visually striking, there are several areas where the User Experience (UX) and User Interface (UI) can be tightened up, particularly for mobile WebViews.

### 🐛 Immediate Bug Fixes Needed
1. **Layout Shift on Wallet Balance**: As the user earns coins, the number width changes (e.g., from `99` to `100`), causing the text to horizontally shift adjacent elements.
   - *Fix*: Apply `font-variant-numeric: tabular-nums;` to `.balance-display` to ensure numbers take up a fixed width.
2. **Text-Only Mode Sizing Issue**: The `.text-only-mode` override forces `height: 400px !important;`. On smaller mobile devices, this rigid height risks bleeding off the screen or overlapping the navbar.
   - *Fix*: Change to `min-height: 400px; height: auto; max-height: 60vh;` to allow flexible scaling.
3. **Form Error Accessibility**: Error messages currently appear abruptly via `innerHTML` injection into an empty `div` (e.g., `id="login-error"`).
   - *Fix*: Add an `aria-live="polite"` attribute to error containers for screen readers, and add a CSS keyframe animation (`@keyframes shake / fadeIn`) to draw visual attention when it triggers.

### ✨ UX Enhancements
1. **Standardize Loading States**: Currently, buttons show a small CSS `spinner` on click. For major view transitions (like waiting for the Matchmaking WebSocket), users stare at an empty "radar" or black box.
   - *Recommendation*: Implement "Skeleton Loaders" (shimmering empty boxes) where the camera or chat history will eventually render to make the app feel faster and less broken while loading.
2. **Keyboard Accessibility**: The `.btn` classes lack specific `:focus-visible` styles.
   - *Recommendation*: Add `.btn:focus-visible { outline: 2px solid var(--secondary); outline-offset: 4px; }` so users navigating via keyboard or mobile accessibility tools know what is selected.
3. **Toast Notifications System**:
   - *Recommendation*: Instead of inline error texts scattered throughout the `dash-layout`, implement a centralized "Toast" notification system that slides in from the top-right corner for success/failure events (e.g., "Avatar Saved", "Withdrawal Requested").
4. **Mobile Navigation Overcrowding**:
   - *Recommendation*: On screens `< 600px`, the header currently shows the logo and multiple action buttons. Move secondary actions (like "Settings" or "Log Out") into a hamburger menu or a sticky bottom navigation bar (very common in social apps) to maximize screen real estate for the chat UI.
5. **Micro-Interactions**:
   - *Recommendation*: Add a subtle coin drop or "sparkle" CSS animation on the `.balance-display` element whenever the WebSocket fires the `earnings_update` event so the user feels tangibly rewarded.
