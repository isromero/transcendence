const form = document.getElementById('username');

(async function() {
    try {
      const response = await fetch('http://localhost:8000/api/users/1');
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const data = await response.json();
      console.log("API Response:", data);
      form.textContent = data.username;
      console.log(form);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  })();
  