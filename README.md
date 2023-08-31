# Aram Stats

Aram Stats is a web application designed to provide users with the ability to view their ARAM game statistics over the past year. The project utilizes the Vue.js framework and is built with Vite for a fast and efficient development experience. The application is hosted on Vercel, and the data is stored and managed using a PostgreSQL database hosted on Supabase.

## Features

- View ARAM game statistics over the past year.
- Chart or Card view.
- User-friendly and responsive web interface.

## Technologies Used

- Vue.js: A progressive JavaScript framework for building user interfaces.
- Vite: A fast build tool for modern web development.
- Vercel: A platform for deploying web applications and sites.
- PostgreSQL: A powerful open-source relational database system.
- Supabase: An open-source alternative to Firebase, providing database and authentication solutions.

## Getting Started

To run this project locally, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/aram-stats.git`
2. Navigate to the project directory: `cd aram-stats`
3. Install dependencies: `npm install`
4. PostgreSQL Database Setup:
   - Create a PostgreSQL database on Supabase.
   - In the `getting-started` folder, you'll find the schema for the database in the `schema.sql` file. Use this to set up the necessary tables and structure in your Supabase database.
   - Additionally, you can find a script in the `getting-started` folder to populate the database with data
5. Configure database: Update the database connection settings in `config.js` with your Supabase credentials.
6. Run the development server: `npm run dev`
7. Access the application at `http://localhost:5173`
