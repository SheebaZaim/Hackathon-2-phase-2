import { NextResponse } from 'next/server';

// Mock user data store
let users = [
  { id: 1, email: 'admin@example.com', password_hash: 'hashed_admin_password', created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
];
let nextUserId = 2;

// Simple password hashing simulation
const hashPassword = (password) => `hashed_${password}`;

// Simple token generation simulation
const generateToken = () => `mock_token_${Math.random().toString(36).substr(2, 9)}`;

export async function POST(request) {
  try {
    const { pathname } = new URL(request.url);
    const segments = pathname.split('/');
    const endpoint = segments[segments.length - 1]; // Get the last segment which should be register/login/logout

    if (endpoint === 'register') {
      const { email, password } = await request.json();

      // Check if user already exists
      const existingUser = users.find(user => user.email === email);
      if (existingUser) {
        return NextResponse.json({ detail: 'Email already registered' }, { status: 400 });
      }

      // Create new user
      const newUser = {
        id: nextUserId++,
        email,
        password_hash: hashPassword(password),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      users.push(newUser);

      // Generate token
      const token = generateToken();

      return NextResponse.json({ access_token: token, token_type: 'bearer' }, { status: 201 });
    } else if (endpoint === 'login') {
      const { email, password } = await request.json();

      // Find user
      const user = users.find(user => user.email === email && user.password_hash === hashPassword(password));
      if (!user) {
        return NextResponse.json({ detail: 'Incorrect email or password' }, { status: 401 });
      }

      // Generate token
      const token = generateToken();

      return NextResponse.json({ access_token: token, token_type: 'bearer' });
    } else if (endpoint === 'logout') {
      return NextResponse.json({ message: 'Successfully logged out' });
    } else {
      return NextResponse.json({ detail: 'Invalid endpoint' }, { status: 404 });
    }
  } catch (error) {
    return NextResponse.json({ detail: 'Authentication failed' }, { status: 500 });
  }
}