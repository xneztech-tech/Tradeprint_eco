# Quick Start Guide - User Management

## 🚀 Server is Running!

The development server is now running at: **http://127.0.0.1:8000/**

## 📍 Important URLs

### Frontend (Public Access)
- **User Registration**: http://127.0.0.1:8000/register/
  - Beautiful gradient design
  - Create new user accounts
  - Automatic login after registration

- **Home Page**: http://127.0.0.1:8000/home/

### Backend (Admin Access Only)
- **Admin Login**: http://127.0.0.1:8000/backend/signin/
  
- **User Management**: http://127.0.0.1:8000/backend/users/
  - View all users
  - Search and filter users
  - Edit user details
  - Delete users
  - View user statistics

- **Admin Dashboard**: http://127.0.0.1:8000/backend/admin-dashboard/

## 🎯 Quick Test Steps

### Test Frontend Registration:
1. Open: http://127.0.0.1:8000/register/
2. Fill in the form:
   - First Name: John
   - Last Name: Doe
   - Email: john.doe@example.com
   - Phone: +1234567890
   - Password: Test@123
   - Confirm Password: Test@123
3. Click "Create Account"
4. You'll be automatically logged in and redirected to home

### Test Admin User Management:
1. Login to admin: http://127.0.0.1:8000/backend/signin/
   - Use your admin credentials
2. Navigate to: http://127.0.0.1:8000/backend/users/
3. You should see:
   - List of all users
   - Search box at the top
   - Role filter dropdown
   - Action buttons (View, Edit, Delete)
4. Try the features:
   - Click eye icon to view user details
   - Click pencil icon to edit user
   - Use search to find users
   - Filter by role

## 🎨 Design Features

### Frontend Registration Page:
- ✨ Modern gradient background (purple to pink)
- 🔒 Password strength indicator
- ✅ Real-time validation
- 📱 Fully responsive design
- 🎭 Smooth animations

### Admin User Management:
- 🔍 Real-time search functionality
- 🏷️ Role-based filtering
- 👤 Avatar circles with user initials
- 🎨 Color-coded role badges
- 📊 User statistics display
- ⚡ AJAX-powered actions

## 🔐 Default Admin Credentials

If you need to create an admin user, run:
```bash
python manage.py createsuperuser
```

Then follow the prompts to create your admin account.

## 📊 Database Tables

The system uses these main tables:
- **User** - Authentication and basic info
- **Customer** - Extended profile information
- **Order** - Customer orders
- **OrderItem** - Order line items

## 🛠️ Troubleshooting

### If registration doesn't work:
1. Check if migrations are applied: `python manage.py migrate`
2. Verify the server is running
3. Check browser console for JavaScript errors

### If admin panel doesn't show users:
1. Ensure you're logged in as admin
2. Check user role is 'admin'
3. Verify URL is correct: `/backend/users/`

### If you see "Permission Denied":
- Only users with role='admin' can access user management
- Regular users cannot access backend URLs

## 📝 Next Actions

1. **Test the registration form** at http://127.0.0.1:8000/register/
2. **Login as admin** and check user list
3. **Try all CRUD operations** (Create, Read, Update, Delete)
4. **Test search and filter** functionality
5. **Verify data is saved** in the database

## 🎉 Success Indicators

✅ Registration form loads with gradient design
✅ New users can register successfully
✅ User and Customer records are created
✅ Admin can view user list
✅ Search and filter work correctly
✅ Edit and delete operations function properly
✅ Proper error messages for validation failures

## 📞 Support

If you encounter any issues:
1. Check the terminal for error messages
2. Review the browser console for JavaScript errors
3. Verify all files are saved
4. Ensure migrations are up to date
5. Check that URLs are correctly configured

---

**Happy Testing! 🚀**
