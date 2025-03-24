document.addEventListener('DOMContentLoaded', () => {
    const options = document.querySelectorAll('.options button');
    const formContainer = document.getElementById('formContainer');
    const formTitle = document.getElementById('formTitle');
    const reportForm = document.getElementById('reportForm');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const chatbotInput = document.getElementById('chatbotInput');
    const sendMessageButton = document.getElementById('sendMessage');
  
    // Hiển thị form khi chọn tùy chọn
    options.forEach(button => {
      button.addEventListener('click', () => {
        formTitle.textContent = `Report ${button.textContent} Issue`;
        formContainer.style.display = 'block';
      });
    });
  
    // Xử lý submit form
    reportForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const issueDescription = document.getElementById('issueDescription').value;
      alert(`Issue reported: ${issueDescription}`);
      reportForm.reset();
      formContainer.style.display = 'none';
    });
  
    // Tích hợp chatbot
    sendMessageButton.addEventListener('click', async () => {
      const message = chatbotInput.value;
      if (!message) return;
  
      // Hiển thị tin nhắn của người dùng
      chatbotMessages.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
  
      // Gọi API Python backend
      try {
        const response = await fetch('http://127.0.0.1:5000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message }),
        });
  
        const data = await response.json();
        if (data.message) {
          // Hiển thị phản hồi của chatbot
          chatbotMessages.innerHTML += `<div><strong>Bot:</strong> ${data.message}</div>`;
        } else {
          chatbotMessages.innerHTML += `<div><strong>Bot:</strong> Sorry, something went wrong.</div>`;
        }
      } catch (error) {
        console.error('Error:', error);
        chatbotMessages.innerHTML += `<div><strong>Bot:</strong> Sorry, something went wrong.</div>`;
      }
  
      // Xóa input và cuộn xuống dưới cùng
      chatbotInput.value = '';
      chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    });
  });