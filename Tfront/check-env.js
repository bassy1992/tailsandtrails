// Check environment variables
console.log('🔍 Environment Variables Check');
console.log('================================');
console.log('NODE_ENV:', process.env.NODE_ENV);
console.log('VITE_API_BASE_URL:', process.env.VITE_API_BASE_URL);
console.log('VITE_API_URL:', process.env.VITE_API_URL);
console.log('');

// Check if .env.production exists and is being loaded
import { readFileSync } from 'fs';
import { join } from 'path';

try {
  const envProd = readFileSync('.env.production', 'utf8');
  console.log('📄 .env.production contents:');
  console.log(envProd);
} catch (e) {
  console.log('❌ .env.production not found or not readable');
}

try {
  const envLocal = readFileSync('.env', 'utf8');
  console.log('📄 .env contents:');
  console.log(envLocal);
} catch (e) {
  console.log('❌ .env not found or not readable');
}