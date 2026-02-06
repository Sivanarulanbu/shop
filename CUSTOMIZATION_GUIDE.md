# 🎨 Customization Guide - Swiftbuy Frontend

## Quick Color Changes

Want to change the color scheme? It's super easy! All colors are defined as CSS variables at the top of `style.css`.

### Change Primary Color (Brand Color)

Open `/static/css/style.css` and find the `:root` section at the top. Change these values:

```css
/* Current: Purple/Indigo */
--primary: #6366f1;
--primary-dark: #4f46e5;
--primary-light: #a5b4fc;
--primary-ultra-light: #e0e7ff;

/* Example: Blue */
--primary: #3b82f6;
--primary-dark: #2563eb;
--primary-light: #93c5fd;
--primary-ultra-light: #dbeafe;

/* Example: Teal */
--primary: #14b8a6;
--primary-dark: #0f766e;
--primary-light: #5eead4;
--primary-ultra-light: #ccfbf1;

/* Example: Orange */
--primary: #f59e0b;
--primary-dark: #d97706;
--primary-light: #fcd34d;
--primary-ultra-light: #fef3c7;
```

### Change Gradient

```css
/* Current: Purple Gradient */
--gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Example: Blue Gradient */
--gradient-primary: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);

/* Example: Warm Gradient */
--gradient-primary: linear-gradient(135deg, #fa709a 0%, #fee140 100%);

/* Example: Cool Gradient */
--gradient-primary: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
```

---

## Customize Hero Section

### Change Hero Text

Open `/shop/templates/shop/product_list.html` and find the hero section:

```html
<h1 class="hero-title">
    Your Main Headline Here
    <span class="hero-gradient-text">Your Gradient Text Here</span>
</h1>
<p class="hero-subtitle">Your subtitle description here</p>
```

### Change Hero Stats

```html
<div class="stat-item">
    <div class="stat-number">Your Number</div>
    <div class="stat-label">Your Label</div>
</div>
```

### Change Hero Colors

In the `<style>` section within `product_list.html`:

```css
.hero-section {
    /* Change gradient background */
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Or use your custom gradient */
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

---

## Customize Fonts

### Change Font Family

In `/shop/templates/shop/base.html`, update the Google Fonts import:

```html
<!-- Current Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<!-- Example: Using Poppins and Montserrat -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=Montserrat:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
```

Then in `style.css`:

```css
body {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Montserrat', sans-serif;
}
```

---

## Customize Shadows

Want more or less shadow? Adjust in `style.css`:

```css
/* Subtle shadows (minimal) */
--shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.08);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.08);

/* Medium shadows (current) */
--shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

/* Strong shadows (dramatic) */
--shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
--shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
--shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.25);
```

---

## Customize Border Radius

Want sharper or rounder corners?

```css
/* Current: Moderate Roundness */
--radius: 10px;
--radius-lg: 16px;
--radius-xl: 20px;

/* Sharp (minimal roundness) */
--radius: 4px;
--radius-lg: 8px;
--radius-xl: 12px;

/* Very Round */
--radius: 16px;
--radius-lg: 24px;
--radius-xl: 32px;
```

---

## Customize Animations

### Speed Up/Slow Down Animations

```css
/* Current: Normal speed */
--transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* Faster */
--transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);

/* Slower */
--transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
```

### Disable Animations (for accessibility)

Add this to your CSS:

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}
```

---

## Customize Product Cards

### Change Hover Effect Strength

In `style.css`, find `.product-card:hover`:

```css
/* Current: Lift and scale */
.product-card:hover {
    transform: translateY(-12px) scale(1.02);
}

/* Subtle */
.product-card:hover {
    transform: translateY(-5px) scale(1.01);
}

/* Dramatic */
.product-card:hover {
    transform: translateY(-20px) scale(1.05);
}
```

### Change Card Background

```css
.product-card {
    background: var(--white); /* Solid white */
    /* OR */
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); /* Gradient */
}
```

---

## Customize Button Styles

### Change Button Roundness

```css
.btn-premium,
.btn-primary {
    border-radius: var(--radius-full); /* Fully rounded */
    /* OR */
    border-radius: var(--radius); /* Moderate */
    /* OR */
    border-radius: 0; /* Square */
}
```

### Change Button Size

```css
/* Current */
.btn-premium {
    padding: 12px 30px;
    font-size: 14px;
}

/* Larger */
.btn-premium {
    padding: 16px 40px;
    font-size: 16px;
}

/* Smaller */
.btn-premium {
    padding: 8px 20px;
    font-size: 12px;
}
```

---

## Quick Tips

### 1. **Test Changes Locally**
Always test your changes in a local development environment before deploying.

### 2. **Cache Busting**
After making changes, update the version number in `base.html`:
```html
<link rel="stylesheet" href="{% static 'css/style.css' %}?v=4.1">
```

### 3. **Run Collectstatic**
After CSS changes, run:
```bash
python manage.py collectstatic --noinput
```

### 4. **Browser DevTools**
Use browser DevTools (F12) to test colors and styles live before committing.

### 5. **Color Tools**
Use tools like:
- [Coolors.co](https://coolors.co) - Generate color palettes
- [ColorHunt](https://colorhunt.co) - Trending color combinations
- [Gradient Generator](https://cssgradient.io) - Create custom gradients

### 6. **Accessibility**
Always check color contrast ratios using tools like:
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

---

## Common Customizations

### Make it More "Corporate"
- Use blues and grays
- Reduce gradients
- Use more whites and subtle shadows
- More spacing, cleaner

```css
--primary: #1e40af; /* Corporate Blue */
--gradient-primary: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
```

### Make it More "Playful"
- Use bright, vibrant colors
- More gradients
- Stronger animations
- Rounded corners

```css
--primary: #ec4899; /* Bright Pink */
--gradient-primary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
--radius: 20px;
```

### Make it More "Luxury"
- Use golds and blacks
- Subtle animations
- More shadows
- Elegant typography

```css
--primary: #d97706; /* Gold */
--gradient-primary: linear-gradient(135deg, #fbbf24 0%, #d97706 100%);
/* Use serif fonts like Playfair Display */
```

---

## Need Help?

- **CSS not updating?** Clear browser cache (Ctrl+Shift+Del)
- **Colors look wrong?** Check if gradients support your browser
- **Animations choppy?** Reduce complexity or use simpler transitions
- **Layout broken?** Check responsive breakpoints

---

**Happy Customizing! 🎨**
