// Import Required Modules
const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const User = require('./models/user');

dotenv.config();
const app = express();
const PORT = process.env.PORT || 8008;

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
    .then(() => console.log('✅ Connected to MongoDB'))
    .catch(err => console.error('❌ MongoDB Connection Error:', err));

// Middleware
app.use(express.json());

// Route to Fetch Today's Birthdays
app.get('/birthdays-today', async (req, res) => {
    try {
        const today = new Date();
        const todayDay = today.getDate();
        const todayMonth = today.getMonth() + 1;

        const birthdays = await User.aggregate([
            {
                $addFields: {
                    birthDateObj: {
                        $dateFromString: {
                            dateString: "$birthdate",
                            format: "%Y-%m-%d" // Adjust format if needed
                        }
                    }
                }
            },
            {
                $match: {
                    $expr: {
                        $and: [
                          { $eq: [ { $dayOfMonth: "$birthDateObj" }, todayDay ] },
                          { $eq: [ { $month: "$birthDateObj" }, todayMonth ] }
                          // Remove message_sent check for now
                        ]
                      }
                      
                }
            }
        ]);

        if (birthdays.length === 0) {
            return res.status(404).send('No birthdays found today.');
        }

        res.json(birthdays);

    } catch (error) {
        console.error('Error fetching birthdays:', error);
        res.status(500).send('Internal Server Error');
    }
});


// Start the Server
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
