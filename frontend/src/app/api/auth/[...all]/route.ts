/**
 * Better Auth API Route
 * Handles all Better Auth endpoints
 */

import { auth } from "@/lib/auth";

export const { GET, POST } = auth.handler;
