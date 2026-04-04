// filepath: /Users/rushilpatel/Desktop/Github/CivicPulse/server/controllers/testClassifierController.js
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');

async function testClassify(req, res) {
  // Extract tags and other potential metadata if needed (optional for dummy)
  const { tags, metadata } = req.body;
  const imageFile = req.file; // Access the uploaded file info via multer

  console.log('Received test classification request.');
  console.log('Tags:', tags); // Log received tags (will likely be a string)
  console.log('Metadata:', metadata); // Log received metadata (if sent)
  console.log('Image File:', imageFile); // Log file details

  // Simulate processing delay (optional)
  await new Promise(resolve => setTimeout(resolve, 50)); // 50ms delay

  // Clean up the uploaded dummy file
  if (imageFile && imageFile.path) {
    fs.unlink(imageFile.path, (err) => {
      if (err) {
        console.error('Error deleting test file:', err);
      } else {
        console.log('Test file deleted:', imageFile.path);
      }
    });
  }

  // Construct the dummy MCP response
  const dummyResponse = {
    request_id: req.body.request_id || uuidv4(), // Use provided ID or generate one
    results: {
      department: {
        prediction: "Road", // Dummy data
        confidence: 0.92,
        model_info: "dept-vit-v1.3-multimodal-dummy"
      },
      severity: {
        prediction: "high", // Dummy data
        confidence: 0.85,
        model_info: "sev-vit-v1.1-multimodal-dummy"
      },
      caption: {
        text: "Large pothole observed on road surface.", // Dummy data
        model_info: "caption-blip-mini-v1-dummy" // Fixed key
      },
      suggested_fixes: [ // Fixed key
        "Assess structural integrity.",
        "Fill with appropriate asphalt mix.",
        "Compact and level the surface."
      ]
    },
    processing_time_ms: 50 // Simulated time
  };

  // Send the dummy response
  res.status(200).json(dummyResponse);
}

module.exports = {
  testClassify,
};