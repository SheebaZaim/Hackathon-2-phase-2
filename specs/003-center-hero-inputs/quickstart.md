# Quickstart Guide: Center Hero Inputs

## Overview
This guide provides instructions for implementing the hero section optimization with centered inputs and proper spacing.

## Prerequisites
- Node.js v16+ installed
- Next.js project set up
- Tailwind CSS or similar CSS framework configured
- Access to original hero section code

## Setup Instructions

### 1. Clone/Access the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Navigate to the Feature Branch
```bash
git checkout 003-center-hero-inputs
```

## Implementation Steps

### Step 1: Create Component Structure
Create the following directory and files:
```
frontend/src/app/components/HeroSection/
├── HeroSection.jsx
├── HeroImage.jsx
└── InputContainer.jsx
```

### Step 2: Implement Image Optimization
1. Place optimized images in `public/images/hero/`
2. Use WebP format with fallbacks
3. Implement responsive images with appropriate sizes

Example:
```jsx
// HeroImage.jsx
import Image from 'next/image';

export default function HeroImage({ src, alt, priority = false }) {
  return (
    <div className="relative w-full h-64 md:h-96">
      <Image
        src={`/images/hero/${src}`}
        alt={alt}
        layout="fill"
        objectFit="cover"
        priority={priority}
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      />
    </div>
  );
}
```

### Step 3: Create Centered Input Container
1. Implement flexbox-based centering
2. Add proper padding and margins
3. Ensure responsive behavior

Example:
```jsx
// InputContainer.jsx
import { useState } from 'react';

export default function InputContainer({ placeholder, buttonText, onSubmit }) {
  const [inputValue, setInputValue] = useState('');
  const [isValid, setIsValid] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim().length >= 2) {
      onSubmit(inputValue);
      setIsValid(true);
    } else {
      setIsValid(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4 sm:p-6">
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={placeholder}
          className={`flex-grow px-4 py-3 rounded-lg border ${
            isValid ? 'border-gray-300' : 'border-red-500'
          } focus:outline-none focus:ring-2 focus:ring-blue-500`}
        />
        <button
          type="submit"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {buttonText}
        </button>
      </form>
      {!isValid && (
        <p className="mt-2 text-red-500 text-sm">Input must be at least 2 characters</p>
      )}
    </div>
  );
}
```

### Step 4: Integrate Components
1. Update the main HeroSection component
2. Apply responsive styling
3. Ensure proper spacing on all screen sizes

Example:
```jsx
// HeroSection.jsx
import HeroImage from './HeroImage';
import InputContainer from './InputContainer';

export default function HeroSection({ title, subtitle, imageSrc, placeholder, buttonText, onSubmit }) {
  return (
    <section className="relative w-full overflow-hidden bg-gray-50">
      <HeroImage src={imageSrc} alt={title} priority={true} />
      
      <div className="absolute inset-0 flex flex-col items-center justify-center p-4 sm:p-8">
        <div className="text-center mb-8 max-w-2xl">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white drop-shadow-lg">
            {title}
          </h1>
          <p className="mt-4 text-lg sm:text-xl text-white drop-shadow-md">
            {subtitle}
          </p>
        </div>
        
        <InputContainer 
          placeholder={placeholder}
          buttonText={buttonText}
          onSubmit={onSubmit}
        />
      </div>
    </section>
  );
}
```

### Step 5: Add Responsive Styling
Add the following CSS to ensure proper centering and spacing across devices:

```css
/* In your global CSS or component-specific CSS */
.hero-centered-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-left: 1rem;
  padding-right: 1rem;
  width: 100%;
}

@media (min-width: 640px) {
  .hero-centered-container {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

@media (min-width: 1024px) {
  .hero-centered-container {
    padding-left: 3rem;
    padding-right: 3rem;
  }
}
```

## Testing

### Manual Testing
1. Verify images load properly on different screen sizes
2. Check that input elements are centered on all devices
3. Confirm proper padding/margin on both sides
4. Test form submission functionality
5. Validate accessibility features

### Automated Testing
Run the following commands to execute tests:
```bash
npm run test
# or for end-to-end tests
npm run test:e2e
```

## Performance Verification
1. Measure page load time before and after implementation
2. Verify image sizes are reduced by at least 30%
3. Check that layout remains responsive across devices
4. Confirm no performance regressions

## Deployment
1. Merge changes to development branch
2. Test in staging environment
3. Deploy to production after approval