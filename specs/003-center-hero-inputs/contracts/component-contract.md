# Component Contract: HeroSection

## Overview
This contract defines the interface and behavior of the HeroSection component that implements the centered inputs and optimized images feature.

## Component Interface

### HeroSection Props
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| title | string | Yes | Main heading text displayed in the hero section |
| subtitle | string | No | Subheading text displayed below the main title |
| imageSrc | string | Yes | Source path for the hero image (relative to public/images/hero/) |
| placeholder | string | Yes | Placeholder text for the input field |
| buttonText | string | Yes | Text displayed on the submit button |
| onSubmit | function | Yes | Callback function called when form is submitted with input value |
| isLoading | boolean | No | Controls loading state of the submit button (default: false) |

### Component Behavior
- The component must render a hero section with an optimized background image
- Input field and submit button must be horizontally centered
- Proper padding must be applied on both sides of the input container
- Responsive design must work across mobile, tablet, and desktop screens
- Form validation must ensure input is at least 2 characters
- Accessibility attributes must be properly set for screen readers

### Expected States
- **Idle**: Normal state with input field ready for user interaction
- **Submitting**: Submit button shows loading indicator when form is being processed
- **Error**: Shows validation error when input doesn't meet requirements
- **Success**: Temporary state after successful submission (handled by parent)

## CSS Classes Contract
The component expects the following CSS classes to be available:

| Class | Purpose |
|-------|---------|
| `hero-centered-container` | Main container with centering and responsive padding |
| `hero-input-field` | Styled input field with proper focus states |
| `hero-submit-button` | Styled submit button with hover/active states |
| `validation-error` | Error message styling |

## Accessibility Requirements
- All interactive elements must be keyboard accessible
- Proper ARIA attributes for dynamic content
- Sufficient color contrast (minimum 4.5:1 ratio)
- Focus indicators must be visible
- Semantic HTML elements must be used appropriately

## Performance Requirements
- Image loading should not block page rendering
- Component should render within 100ms of being mounted
- Image file sizes should be reduced by at least 30% compared to original
- Page load time improvement of at least 20% after image optimization

## Responsive Breakpoints
- Mobile: Up to 768px screen width
- Tablet: 768px to 1024px screen width
- Desktop: Above 1024px screen width

## Dependencies
- Next.js Image component for optimized image loading
- Tailwind CSS or similar framework for utility classes
- React 17+ for component implementation