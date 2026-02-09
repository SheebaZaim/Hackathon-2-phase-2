import { useState } from 'react';

const InputContainer = ({ placeholder, buttonText, onSubmit, inputValue, setInputValue }) => {
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
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
        >
          {buttonText}
        </button>
      </form>
      {!isValid && (
        <p className="mt-2 text-red-300 text-sm">Input must be at least 2 characters</p>
      )}
    </div>
  );
};

export default InputContainer;