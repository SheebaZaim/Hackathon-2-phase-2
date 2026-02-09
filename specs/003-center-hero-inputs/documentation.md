# Center Hero Inputs Feature Documentation

## Overview
This feature optimizes the frontend hero section by minimizing image sizes and centering input elements with appropriate padding and margins on both sides of the page. This improves page loading times and enhances the visual appeal of the user interface.

## Components

### HeroSection Component
The main container for the hero section with the following props:
- `title` (string): Main heading text
- `subtitle` (string): Subheading text
- `imageSrc` (string): Source path for the hero image
- `placeholder` (string): Placeholder text for the input field
- `buttonText` (string): Text displayed on the submit button
- `onSubmit` (function): Callback function called when form is submitted
- `isLoading` (boolean): Controls loading state of the submit button

### InputContainer Component
Contains input elements with centered layout:
- Handles form submission
- Manages validation state
- Provides visual feedback for validation errors

## Responsive Design
The layout is responsive across different device sizes:
- Mobile: Up to 768px screen width
- Tablet: 768px to 1024px screen width
- Desktop: Above 1024px screen width

## Accessibility Features
- Proper ARIA attributes for screen readers
- Sufficient color contrast (meets WCAG 2.1 AA standards)
- Keyboard navigation support
- Focus indicators for interactive elements

## Performance Improvements
- Images are optimized using WebP format with fallbacks
- Image file sizes reduced by at least 30%
- Page load time improved by reducing image payload
- Lazy loading implemented for non-critical images

## Usage Example

```jsx
import HeroSection from './components/HeroSection/HeroSection';

function App() {
  const handleSubmit = (value) => {
    console.log('Form submitted with value:', value);
  };

  return (
    <div className="App">
      <HeroSection
        title="Welcome to Our Service"
        subtitle="Experience the best with our solution"
        imageSrc="hero-background.webp"
        placeholder="Enter your email"
        buttonText="Get Started"
        onSubmit={handleSubmit}
      />
    </div>
  );
}
```

## Testing
Unit tests are available in `tests/unit/components/HeroSection.test.js`
End-to-end tests are available in `tests/e2e/hero-section.cy.js`

Run unit tests with: `npm run test:unit`
Run e2e tests with: `npm run test:e2e`