# Data Model: Center Hero Inputs

## Overview
This document outlines the component structure and data flow for the hero section optimization feature. Since this is primarily a UI/frontend change, the "data model" focuses on component interfaces and state management.

## Component Structure

### HeroSection Component
- **Purpose**: Main container for the hero section
- **Props**:
  - `title` (string): Main heading text
  - `subtitle` (string): Subheading text
  - `ctaText` (string): Call-to-action button text
  - `onSubmit` (function): Handler for form submission
  - `isLoading` (boolean): Loading state indicator
- **State**:
  - `inputValue` (string): Current value of input field
  - `isFocused` (boolean): Tracks input focus state
- **Children**: HeroImage, InputContainer

### HeroImage Component
- **Purpose**: Displays optimized hero section image
- **Props**:
  - `src` (string): Image source URL
  - `alt` (string): Alt text for accessibility
  - `priority` (boolean): Whether to prioritize loading (Next.js)
- **State**: None
- **Children**: None

### InputContainer Component
- **Purpose**: Contains input elements with centered layout
- **Props**:
  - `placeholder` (string): Input placeholder text
  - `buttonText` (string): Submit button text
  - `onSubmit` (function): Handler for form submission
- **State**:
  - `inputValue` (string): Current value of input field
  - `isValid` (boolean): Validation state
- **Children**: InputField, SubmitButton

### InputField Component
- **Purpose**: Input element with proper styling and validation
- **Props**:
  - `placeholder` (string): Placeholder text
  - `value` (string): Current value
  - `onChange` (function): Value change handler
  - `isValid` (boolean): Validation state
- **State**: None
- **Children**: None

### SubmitButton Component
- **Purpose**: Submit button with loading state
- **Props**:
  - `text` (string): Button text
  - `onClick` (function): Click handler
  - `isLoading` (boolean): Loading state
- **State**: None
- **Children**: None

## State Transitions

### Input Field
- `initial` → `focused` when user clicks/focuses on input
- `focused` → `valid` when input meets validation criteria
- `focused` → `invalid` when input fails validation
- `valid/invalid` → `submitted` when form is submitted

### Form Submission
- `idle` → `submitting` when submit button is clicked
- `submitting` → `success` when submission succeeds
- `submitting` → `error` when submission fails
- `success/error` → `idle` when user performs new action

## Validation Rules

### Input Field Validation
- Required: Field must not be empty
- Length: Minimum 2 characters, maximum 100 characters
- Format: Should match expected input type (email, text, etc.)

### Accessibility Compliance
- All interactive elements must have proper ARIA labels
- Color contrast must meet WCAG 2.1 AA standards
- Keyboard navigation must be fully supported

## Styling Properties

### Container Spacing
- `padding-inline`: 1rem on mobile, 2rem on tablet, 3rem on desktop
- `margin-block`: 1rem top/bottom on mobile, 2rem on larger screens
- `max-width`: 1200px centered container

### Centering Properties
- `display`: flex
- `justify-content`: center
- `align-items`: center
- `text-align`: center (for text elements)

### Responsive Breakpoints
- Mobile: up to 768px
- Tablet: 768px to 1024px
- Desktop: 1024px and above