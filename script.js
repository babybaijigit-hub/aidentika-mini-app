document.addEventListener("DOMContentLoaded", () => {
  const tg = window.Telegram?.WebApp;
  const form = document.getElementById("requestForm");
  const result = document.getElementById("result");
  const resultText = document.getElementById("resultText");

  if (tg) {
    tg.ready();
    tg.expand();
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const data = {
      type: document.getElementById("type").value,
      topic: document.getElementById("topic").value.trim(),
      subject: document.getElementById("subject").value.trim(),
      requirements: document.getElementById("requirements").value.trim()
    };

    if (!data.topic || !data.subject) {
      form.reportValidity();
      return;
    }

    resultText.textContent = [
      `Тип: ${data.type}`,
      `Тема: ${data.topic}`,
      `Предмет: ${data.subject}`,
      `Требования: ${data.requirements || "не указаны"}`
    ].join("\n");
    result.hidden = false;

    // sendData works when the Mini App was opened from a Telegram bot keyboard.
    if (tg) {
      tg.sendData(JSON.stringify(data));
    }
  });
});
