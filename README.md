# CivicFix Backend API

Node.js + Express + MongoDB REST API for the CivicFix civic issue reporting platform.

---

## 📁 Project Structure

```
civicfix-backend/
├── src/
│   ├── index.js                  # Entry point – Express app & server
│   ├── config/
│   │   └── db.js                 # MongoDB connection
│   ├── models/
│   │   ├── Issue.js              # Issue schema (GeoJSON + reactions)
│   │   └── GovtUpdate.js         # Government resolution post schema
│   ├── routes/
│   │   ├── issues.js             # CRUD + geospatial + react endpoints
│   │   ├── govtUpdates.js        # Govt resolution posts
│   │   └── analytics.js          # Admin dashboard aggregations
│   └── middleware/
│       └── errorHandler.js       # Global error handler
├── .env                          # Environment variables (edit before running)
├── package.json
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** ≥ 18
- **MongoDB** running locally **or** a MongoDB Atlas connection string

### 1. Install dependencies
```bash
cd civicfix-backend
npm install
```

### 2. Configure environment
Edit `.env`:
```env
# Local MongoDB
MONGO_URI=mongodb://127.0.0.1:27017/civicfix

# OR MongoDB Atlas
# MONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/civicfix

PORT=5000
NODE_ENV=development
```

### 3. Start the server
```bash
# Production
npm start

# Development (auto-restart on file changes)
npm run dev
```

Server starts at **http://localhost:5000**

---

## 🌐 API Reference

### Health Check
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Server + DB status |

---

### Issues

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/issues` | List issues (with optional geo-filter) |
| POST | `/api/issues` | Create a new issue |
| GET | `/api/issues/:id` | Get a single issue |
| PATCH | `/api/issues/:id` | Update status / resolution note |
| DELETE | `/api/issues/:id` | Delete an issue |
| POST | `/api/issues/:id/react` | Toggle a reaction (seen / serious) |

#### GET `/api/issues` – Query Parameters
| Param | Type | Description |
|-------|------|-------------|
| `lat` | float | User latitude – enables geospatial sort |
| `lng` | float | User longitude |
| `radius` | number | Search radius in km (default: 10) |
| `category` | string | Filter by category |
| `status` | string | Filter by status |
| `limit` | number | Results per page (default: 50) |
| `page` | number | Page number (default: 1) |

#### POST `/api/issues` – Request Body
```json
{
  "title": "Broken Street Light",
  "desc": "Street light out on main road for 5 days.",
  "category": "Lighting",
  "lat": 23.2599,
  "lng": 77.4126,
  "locationText": "MG Road, Bhopal",
  "reporter": "Rahul S.",
  "photoUrl": "data:image/jpeg;base64,..."
}
```

#### PATCH `/api/issues/:id` – Request Body
```json
{
  "status": "In Progress",
  "resolutionNote": "Crew dispatched. ETA 2 days."
}
```

#### POST `/api/issues/:id/react` – Request Body
```json
{
  "type": "seen",
  "userId": "Rahul S."
}
```
Response includes `action` (`"added"` | `"removed"`) and updated `reactionCounts`.

---

### Government Updates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/govt-updates` | List all updates (filter by `?issueId=`) |
| POST | `/api/govt-updates` | Post a resolution update |
| DELETE | `/api/govt-updates/:id` | Remove an update |

#### POST `/api/govt-updates` – Request Body
```json
{
  "issueId": "64abc...",
  "dept": "Nagar Palika – Roads",
  "by": "Officer Sharma",
  "note": "Pothole filled with hot mix asphalt.",
  "workBy": "PWD Contractor",
  "photoUrl": "data:image/jpeg;base64,...",
  "status": "Resolved"
}
```

---

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/summary` | Aggregated stats for admin dashboard |

Response:
```json
{
  "success": true,
  "data": {
    "total": 120,
    "resolved": 45,
    "urgent": 12,
    "inProgress": 18,
    "resolutionRate": 37,
    "byCategory": { "Infrastructure": 30, "Sanitation": 25, ... },
    "byStatus": { "Reported": 57, "In Progress": 18, ... }
  }
}
```

---

## 🗄️ MongoDB Schema

### Issue
| Field | Type | Notes |
|-------|------|-------|
| `title` | String | Max 200 chars |
| `desc` | String | Max 2000 chars |
| `category` | String | Enum: Infrastructure, Sanitation, Utilities, Lighting, Vandalism, Other |
| `status` | String | Enum: Reported, Verified, In Progress, Resolved |
| `urgency` | String | Enum: low, medium, high – auto-updated on reactions |
| `location` | GeoJSON Point | `{ type: "Point", coordinates: [lng, lat] }` – 2dsphere indexed |
| `locationText` | String | Human-readable address |
| `reporter` | String | Username |
| `photoUrl` | String | base64 data URL or hosted URL |
| `resolutionNote` | String | Filled by Govt / Admin |
| `reactions` | Array | `[{ userId, type }]` – one per user+type |
| `reactionCounts` | Object | `{ seen: N, serious: N }` – denormalised for fast reads |
| `createdAt` | Date | Auto (timestamps) |
| `updatedAt` | Date | Auto (timestamps) |

### GovtUpdate
| Field | Type | Notes |
|-------|------|-------|
| `issueId` | ObjectId | Ref → Issue |
| `dept` | String | Department name |
| `by` | String | Official name |
| `note` | String | Resolution note |
| `workBy` | String | Contractor / team |
| `photoUrl` | String | Proof-of-fix image |
| `status` | String | New status applied |
| `createdAt` | Date | Auto |

---

## 🔧 Connecting the Frontend

The frontend HTML already calls `http://localhost:5000/api` via the `API_BASE` constant.

**No changes needed in the frontend** – just start this backend and open the HTML file in your browser.

If deploying to a remote server, update `API_BASE` in the HTML:
```js
const API_BASE = 'https://your-server.com/api';
```

---

## ☁️ MongoDB Atlas (Cloud)

1. Create a free cluster at [cloud.mongodb.com](https://cloud.mongodb.com)
2. Add a database user and whitelist your IP
3. Copy the connection string and paste into `.env`:
```env
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/civicfix?retryWrites=true&w=majority
```

---

## 🚢 Deploying to Production

### Render / Railway / Fly.io
1. Push the `civicfix-backend` folder to GitHub
2. Create a new Web Service pointing to it
3. Set environment variables (`MONGO_URI`, `PORT`, `NODE_ENV=production`)
4. Build command: `npm install` | Start command: `npm start`

### With PM2 on a VPS
```bash
npm install -g pm2
pm2 start src/index.js --name civicfix-api
pm2 save && pm2 startup
```
