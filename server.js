const fs = require("fs");
const path = require("path");
const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

const DATA_FILE = path.join(__dirname, "utils", "dealers.json");

function readDealerData() {
  try {
    const parsed = JSON.parse(fs.readFileSync(DATA_FILE, "utf8"));
    return Array.isArray(parsed) ? parsed : (parsed.dealers || []);
  } catch (err) {
    console.error("Unable to read dealer data:", err.message);
    return [];
  }
}

function normalizeDealer(d, index) {
  return {
    id: Number(d.id) || index + 1,
    name: d.name || d.Dealer || d.full_name || "Unnamed dealer",
    short_name: d.short_name || d.name || d.Dealer || "",
    city: d.city || "",
    state: d.state || "",
    address: d.address || "",
    zip: d.zip || "",
    lat: d.lat || "",
    long: d.long || "",
    products: d.products || {}
  };
}

app.get("/alldealers", (req, res) => {
  res.json({ dealers: readDealerData().map(normalizeDealer) });
});

app.get("/fetchDealers", (req, res) => {
  const dealers = readDealerData().map((d, index) => ({
    id: Number(d.id) || index + 1,
    short_name: d.short_name || d.name || d.Dealer || "",
    full_name: d.full_name || d.name || d.Dealer || "",
    city: d.city || "",
    state: d.state || "",
    address: d.address || "",
    zip: d.zip || "",
    latitude: d.latitude || d.lat || "",
    longitude: d.longitude || d.long || ""
  }));

  res.json({ dealers });
});


app.get("/dealerbyid/:id", (req, res) => {
  const dealer = readDealerData().map(normalizeDealer)
    .find(d => String(d.id) === String(req.params.id));
  if (!dealer) return res.status(404).json({ message: "Dealer not found" });
  res.json(dealer);
});

app.get("/dealersbyState/:state", (req, res) => {
  const state = req.params.state.toLowerCase();
  const dealers = readDealerData().map(normalizeDealer)
    .filter(d => d.state.toLowerCase() === state);
  res.json({ dealers });
});

app.get("/price/:dealer/:product", (req, res) => {
  const dealer = readDealerData().map(normalizeDealer)
    .find(d => d.name.toLowerCase() === req.params.dealer.toLowerCase());
  if (!dealer) return res.status(404).json({ message: "Dealer not found" });
  const key = Object.keys(dealer.products)
    .find(k => k.toLowerCase() === req.params.product.toLowerCase());
  if (!key) return res.json({ message: `${req.params.product} is not available with ${dealer.name}` });
  res.json({ message: `${key} costs ${dealer.products[key]} at ${dealer.name}` });
});

app.get("/allprice/:product", (req, res) => {
  const prices = [];
  readDealerData().map(normalizeDealer).forEach(d => {
    const key = Object.keys(d.products)
      .find(k => k.toLowerCase() === req.params.product.toLowerCase());
    if (key) prices.push({ key: d.name, value: d.products[key] });
  });
  if (!prices.length) return res.status(404).json({ message: "Product not available" });
  res.json({ prices });
});

app.post("/login", (req, res) => {
  const { username, password } = req.body || {};
  if (username === "testuser" && password === "Test@123") {
    return res.json({ message: "Login successful", username });
  }
  res.status(401).json({ message: "Invalid username or password" });
});

app.post("/logout", (req, res) => res.json({ message: "Logout successful" }));

const dealerReviews = {
  1: [
    {
      name: "Alex Johnson",
      purchase: "Purchased a laptop",
      car_make: "Toyota",
      car_model: "Camry",
      car_year: 2022,
      review: "Good service and helpful staff",
      rating: 5
    },
    {
      name: "Sam Wilson",
      purchase: "Purchased a desktop computer",
      car_make: "Honda",
      car_model: "Civic",
      car_year: 2021,
      review: "Products were delivered on time",
      rating: 4
    }
  ]
};

app.get("/fetchReviews/dealer/:dealer_id", (req, res) => {
  const dealerId = req.params.dealer_id;

  res.json({
    dealerId,
    reviews: dealerReviews[dealerId] || []
  });
});

app.get("/getallcarmakes", (req, res) => {
  res.json({ carMakes: [
    { make: "Toyota", models: ["Camry", "Corolla"] },
    { make: "Honda", models: ["Civic", "Accord"] },
    { make: "Ford", models: ["Mustang", "Focus"] }
  ] });
});

app.get("/analyzereview", (req, res) => {
  const review = String(req.query.review || "").toLowerCase();
  const positive = ["fantastic", "excellent", "great", "good", "amazing", "helpful", "wonderful"];
  const negative = ["bad", "poor", "terrible", "awful", "worst", "horrible"];
  let sentiment = "neutral";
  if (positive.some(w => review.includes(w))) sentiment = "positive";
  else if (negative.some(w => review.includes(w))) sentiment = "negative";
  res.json({ review: req.query.review || "", sentiment });
});

const port = process.env.PORT || 8080;

app.get("/fetchDealer/:dealer_id", (req, res) => {
  const dealers = readDealerData();
  const dealer = dealers.find(d => String(d.id) === String(req.params.dealer_id));

  if (!dealer) {
    return res.status(404).json({ error: "Dealer not found" });
  }

  res.json({
    id: Number(dealer.id),
    city: dealer.city || "",
    state: dealer.state || "",
    address: dealer.address || "",
    zip: dealer.zip || "",
    lat: dealer.latitude ?? dealer.lat ?? "",
    long: dealer.longitude ?? dealer.long ?? "",
    short_name: dealer.short_name || dealer.name || dealer.Dealer || "",
    full_name: dealer.full_name || dealer.name || dealer.Dealer || ""
  });
});

app.listen(port, () => console.log(`Dealer API listening on port ${port}`));
