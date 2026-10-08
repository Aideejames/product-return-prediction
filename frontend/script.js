// Change this to your deployed backend URL when you host it
const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("order-form");
const resultBox = document.getElementById("result");
const probEl = document.getElementById("prob");
const decisionEl = document.getElementById("decision");
const hintEl = document.getElementById("hint");
const gaugeFill = document.getElementById("gauge-fill");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const fd = new FormData(form);
  const payload = {
    product_category: fd.get("product_category"),
    sub_category: fd.get("sub_category"),
    brand: fd.get("brand"),
    product_price: parseFloat(fd.get("product_price")),
    discount_percent: parseFloat(fd.get("discount_percent")),
    product_rating: parseFloat(fd.get("product_rating")),
    review_count: parseFloat(fd.get("review_count")),
    fragile_item: fd.get("fragile_item") ? 1 : 0,
    warranty_available: fd.get("warranty_available") ? 1 : 0,
    product_return_rate: parseFloat(fd.get("product_return_rate")),
    category_return_rate: parseFloat(fd.get("category_return_rate")),
    brand_return_rate: parseFloat(fd.get("brand_return_rate")),
    defect_rate: parseFloat(fd.get("defect_rate")),
    seller_rating: parseFloat(fd.get("seller_rating")),
    seller_return_rate: parseFloat(fd.get("seller_return_rate")),
    fulfillment_type: fd.get("fulfillment_type"),
    payment_method: fd.get("payment_method"),
    quantity: parseInt(fd.get("quantity")),
    shipping_distance_km: parseFloat(fd.get("shipping_distance_km")),
    delayed_delivery: fd.get("delayed_delivery") ? 1 : 0,
    wishlist_before_purchase: fd.get("wishlist_before_purchase") ? 1 : 0,
    product_page_views: parseInt(fd.get("product_page_views")),
    customer_support_calls: parseInt(fd.get("customer_support_calls")),
    chat_interactions: parseInt(fd.get("chat_interactions")),
  };

  try {
    const res = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json();
      alert(`API error: ${err.detail || res.statusText}`);
      return;
    }

    const data = await res.json();
    const pct = (data.return_probability * 100).toFixed(1);

    probEl.textContent = `${pct}%`;
    decisionEl.textContent = data.predicted_returned
      ? "⚠️ HIGH RISK — flag for intervention"
      : "✅ LOW RISK — ship as normal";
    hintEl.textContent = `Decision threshold: ${data.threshold} · Model: ${data.model_name}`;

    // Gauge — colour shifts with risk
    gaugeFill.style.width = `${pct}%`;
    gaugeFill.style.background =
      data.return_probability > 0.6 ? "#e76f51" :
      data.return_probability > 0.35 ? "#e9c46a" : "#2a9d8f";

    resultBox.classList.remove("hidden");
  } catch (err) {
    alert("Could not reach the API. Is the backend running?");
    console.error(err);
  }
});