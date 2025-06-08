const chatBox = document.getElementById('chat-box');

// 🔒 Authentication Check
const user = localStorage.getItem("user");
if (!user) {
  window.location.href = "login.html";
} else {
  appendMessage("Bot", `Welcome back, ${user}!`);
}

// 🚪 Logout
document.getElementById("logout-btn").onclick = () => {
  localStorage.removeItem("user");
  window.location.href = "login.html";
};

// 💬 Send Chat Message
function sendMessage() {
  const input = document.getElementById('user-input');
  const message = input.value.trim();
  if (!message) return;

  appendMessage('You', message);

  fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  })
    .then(response => response.json())
    .then(data => {
      appendMessage('Bot', data.reply, true);
      if (data.products && data.products.length > 0) {
        renderProductCards(data.products);
      }
    })
    .catch(error => {
      appendMessage('Bot', 'Error contacting server.');
    });

  input.value = '';
}

// 🛒 Local cart logic
function addToCart(name, price) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  cart.push({ name, price });
  localStorage.setItem("cart", JSON.stringify(cart));
  alert(`${name} added to cart!`);
}

function showCart() {
  const cartItemsDiv = document.getElementById("cart-items");
  const cart = JSON.parse(localStorage.getItem("cart")) || [];

  if (cart.length === 0) {
    cartItemsDiv.innerHTML = "<p>Your cart is empty.</p>";
    return;
  }

  cartItemsDiv.innerHTML = "";
  let total = 0;

  cart.forEach((item, index) => {
    total += item.price;
    const div = document.createElement("div");
    div.innerHTML = `
      <p>${index + 1}. ${item.name} - ₹${item.price.toFixed(2)}
        <button onclick="removeCartItem(${index})">Remove</button></p>`;
    cartItemsDiv.appendChild(div);
  });

  const totalDiv = document.createElement("div");
  totalDiv.innerHTML = `<h4>Total: ₹${total.toFixed(2)}</h4>`;
  cartItemsDiv.appendChild(totalDiv);
}

function removeCartItem(index) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  cart.splice(index, 1);
  localStorage.setItem("cart", JSON.stringify(cart));
  showCart();
}


// 🧾 Append Message to Chat
function appendMessage(sender, text, isBot = false) {
  if (!text) text = "Sorry, something went wrong.";
  const msgDiv = document.createElement('div');
  msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  if (isBot && text.toLowerCase().includes("things you can try")) {
    showSuggestions();
  } else {
    document.getElementById("suggestion-box").innerHTML = "";
  }
}

// 📦 Render Products
function renderProductCards(products) {
  products.forEach(product => {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
      <img src="${product.image}" alt="${product.name}" />
      <div class="product-info">
        <strong>${product.name}</strong><br>
        ₹${product.price} ⭐${product.rating}<br>
        <button onclick="addToCart('${product.name}', ${product.price})">Add to Cart</button>

      </div>
    `;
    chatBox.appendChild(card);
    chatBox.scrollTop = chatBox.scrollHeight;
  });
}

// 💡 Suggestion Buttons
function showSuggestions() {
  const commands = ["show mobiles", "search books", "under 1000", "show all", "top rated", "help"];
  const suggestionBox = document.getElementById("suggestion-box");
  suggestionBox.innerHTML = "";

  commands.forEach(cmd => {
    const btn = document.createElement("button");
    btn.innerText = cmd;
    btn.onclick = () => {
      document.getElementById("user-input").value = cmd;
      sendMessage();
    };
    suggestionBox.appendChild(btn);
  });
}
// ✅ Admin Product Form Submission
document.getElementById("product-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const name = document.getElementById("product-name").value;
  const category = document.getElementById("product-category").value;
  const price = parseFloat(document.getElementById("product-price").value);
  const rating = parseFloat(document.getElementById("product-rating").value);

  fetch("http://localhost:5000/add-product", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, category, price, rating }),
  })
    .then((res) => res.json())
    .then((data) => {
      alert(data.message);
      if (data.success) {
        document.getElementById("product-form").reset();
      }
    })
    .catch((err) => alert("Error adding product"));
});

function fetchAdminProducts() {
  fetch("http://localhost:5000/admin-products")
    .then(res => res.json())
    .then(data => {
      const section = document.getElementById("admin-section");
      const list = document.createElement("div");
      list.innerHTML = "<h4>All Products</h4>";

      data.forEach(p => {
        const item = document.createElement("div");
        item.innerHTML = `<p><strong>${p.name}</strong> | ₹${p.price} | ⭐${p.rating} | Category: ${p.category}</p>`;
        list.appendChild(item);
      });

      section.appendChild(list);
    });
}


// 🔀 Section Switch (✅ fixed block)
function showSection(section) {
  document.getElementById("chat-section").style.display = (section === "chat") ? "block" : "none";
  document.getElementById("cart-section").style.display = (section === "cart") ? "block" : "none";
  document.getElementById("admin-section").style.display = (section === "admin") ? "block" : "none";
 if (section === "admin") fetchAdminProducts();

  if (section === "cart") {
    showCart(); // Optional: if you implement cart logic
  }
}

// 🔒 Hide Admin Button If Not Admin
if (user !== "kushaldubey29@gmail.com") {
  const adminBtn = document.querySelector("button[onclick=\"showSection('admin')\"]");
  if (adminBtn) adminBtn.style.display = "none";
  const adminSection = document.getElementById("admin-section");
  if (adminSection) adminSection.style.display = "none";
}
