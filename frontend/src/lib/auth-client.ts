/**
 * Better Auth Client Configuration
 * Handles user authentication with Better Auth
 */

import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000",
});

export const { signIn, signUp, signOut, useSession } = authClient;
