# User Authentication System

This project is a simple user authentication system developed for the Office of Career Services (OCS) at IIT Delhi as part of their technical team recruitment process.

## Features

- User login with client-side password hashing
- Role-based data display (admin sees all users, regular users see only their own data)
- Integration with Supabase for backend services

## Setup

1. Clone this repository
2. Create a Supabase project and set up the database according to the provided schema
3. Update the `SUPABASE_URL` and `SUPABASE_ANON_KEY` in `script.js` with your Supabase project credentials
4. Deploy the project to a hosting service like Vercel

## Technologies Used

- HTML, CSS, JavaScript
- Supabase (Backend as a Service)
- MD5 for client-side password hashing

## Deployment

This project is designed to be easily deployed on Vercel. Simply connect your GitHub repository to Vercel and it will automatically deploy your application.

## Security Considerations

- Passwords are hashed client-side using MD5 before being sent to the server
- All database interactions are handled server-side through Supabase
- No sensitive information is exposed in the frontend code

## Limitations and Future Improvements

- Implement a more secure hashing algorithm (e.g., bcrypt) on the server-side
- Add user registration functionality
- Implement proper session management and JWT authentication
