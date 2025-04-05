document.addEventListener('DOMContentLoaded', () => {
  const options = document.querySelectorAll('.options button');
  const formContainer = document.getElementById('formContainer');
  const formTitle = document.getElementById('formTitle');
  const reportForm = document.getElementById('reportForm');
  const chatbotMessages = document.getElementById('chatbotMessages');
  const chatbotInput = document.getElementById('chatbotInput');
  const sendMessageButton = document.getElementById('sendMessage');
  const imageUpload = document.getElementById('imageUpload');

  options.forEach(button => {
    button.addEventListener('click', () => {
      formTitle.textContent = `Report ${button.textContent} Issue`;
      formContainer.style.display = 'block';
    });
  });

  reportForm.addEventListener('submit', async (e) => {
    e.preventDefault();
  
    const issueDescription = document.getElementById('issueDescription');
    const selectedLocation = document.getElementById('formTitle').textContent.replace("Report ", "").replace(" Issue", "");
  
    let issueText = issueDescription.value;
  
    // STEP 1: Get AI description from image if uploaded
    if (imageUpload.files.length > 0) {
      const formData = new FormData();
      formData.append('image', imageUpload.files[0]);
  
      try {
        const response = await fetch('http://127.0.0.1:5000/image-report', {
          method: 'POST',
          body: formData
        });
  
        const data = await response.json();
        if (data.description) {
          issueText = data.description;
          issueDescription.value = issueText;
          alert(`🧠 AI-detected issue: ${issueText}`);
        } else {
          alert('Could not classify the issue using AI.');
        }
      } catch (error) {
        console.error('Image classification error:', error);
        alert('Something went wrong while analyzing the image.');
      }
    }
  
    // STEP 2: This is where you put the emailResponse fetch:
    try {
      const emailResponse = await fetch('http://127.0.0.1:5000/email-with-ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          issue: issueText,
          location: selectedLocation
        })
      });
  
      const emailResult = await emailResponse.json();
  
      if (emailResult.status) {
        alert("Email sent successfully!\n\n📧 AI-written message:\n\n" + emailResult.email_body);
      } else {
        alert("Failed to send email.");
      }
    } catch (error) {
      console.error('Email send error:', error);
      alert('Something went wrong while sending the email.');
    }
  
    reportForm.reset();
    formContainer.style.display = 'none';
  });
  

  sendMessageButton.addEventListener('click', async () => {
    const message = chatbotInput.value;
    if (!message) return;

    chatbotMessages.innerHTML += `<div><strong>You:</strong> ${message}</div>`;

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
        chatbotMessages.innerHTML += `<div><strong>Bot:</strong> ${data.message}</div>`;
      } else {
        chatbotMessages.innerHTML += `<div><strong>Bot:</strong> Sorry, something went wrong.</div>`;
      }
    } catch (error) {
      console.error('Error:', error);
      chatbotMessages.innerHTML += `<div><strong>Bot:</strong> Sorry, something went wrong.</div>`;
    }

    chatbotInput.value = '';
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
  });
});
