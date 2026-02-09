// HeroSection.test.js
// Unit tests for the HeroSection component

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import HeroSection from '../components/HeroSection/HeroSection';

describe('HeroSection Component', () => {
  const defaultProps = {
    title: 'Welcome to Our Site',
    subtitle: 'The best experience awaits you',
    imageSrc: 'test-image.webp',
    placeholder: 'Enter your email',
    buttonText: 'Subscribe',
    onSubmit: jest.fn()
  };

  beforeEach(() => {
    defaultProps.onSubmit.mockClear();
  });

  test('renders main elements correctly', () => {
    render(<HeroSection {...defaultProps} />);
    
    expect(screen.getByText('Welcome to Our Site')).toBeInTheDocument();
    expect(screen.getByText('The best experience awaits you')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your email')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Subscribe' })).toBeInTheDocument();
  });

  test('handles form submission with valid input', () => {
    render(<HeroSection {...defaultProps} />);
    
    const input = screen.getByPlaceholderText('Enter your email');
    const button = screen.getByRole('button', { name: 'Subscribe' });
    
    fireEvent.change(input, { target: { value: 'test@example.com' } });
    fireEvent.click(button);
    
    expect(defaultProps.onSubmit).toHaveBeenCalledWith('test@example.com');
  });

  test('shows validation error for short input', () => {
    render(<HeroSection {...defaultProps} />);
    
    const input = screen.getByPlaceholderText('Enter your email');
    const button = screen.getByRole('button', { name: 'Subscribe' });
    
    fireEvent.change(input, { target: { value: 'x' } }); // Less than 2 characters
    fireEvent.click(button);
    
    expect(screen.getByText('Input must be at least 2 characters')).toBeInTheDocument();
    expect(defaultProps.onSubmit).not.toHaveBeenCalled();
  });

  test('centers input elements properly', () => {
    render(<HeroSection {...defaultProps} />);
    
    const form = screen.getByRole('form');
    expect(form).toHaveClass('flex');
    expect(form).toHaveClass('flex-col'); // On mobile
  });
});