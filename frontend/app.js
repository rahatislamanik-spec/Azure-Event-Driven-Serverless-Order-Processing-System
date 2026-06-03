const API_ENDPOINT = "https://YOUR-FUNCTION-APP.azurewebsites.net/api/submit_order";

document.getElementById("orderForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const order = {
    firstName: document.getElementById("firstName").value.trim(),
    lastName: document.getElementById("lastName").value.trim(),
    email: document.getElementById("email").value.trim(),
    phone: document.getElementById("phone").value.trim(),
    address: document.getElementById("address").value.trim(),
    productId: document.getElementById("productId").value,
    quantity: Number(document.getElementById("quantity").value)
  };
  const result = document.getElementById("result");
  result.textContent = "Submitting order...";
  try {
    const response = await fetch(API_ENDPOINT, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(order)});
    const data = await response.json();
    result.textContent = response.ok ? `Order received. Order ID: ${data.orderId}` : `Order failed: ${data.error || "Invalid request"}`;
  } catch (error) {
    result.textContent = "Unable to submit order. Please try again later.";
    console.error(error);
  }
});
