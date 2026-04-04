// filepath: /Users/rushilpatel/Desktop/Github/CivicPulse/server/routes/testClassifierRouter.js
const express = require('express');
const router = express.Router();
const testClassifierController = require('../controllers/testClassifierController');

// POST endpoint at the root of this router (will be /api/test-classify/)
router.post('/', testClassifierController.testClassify);

module.exports = router;