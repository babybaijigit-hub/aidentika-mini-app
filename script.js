"""Local structured study plan for the static Mini App (no API key required)."""
document.addEventListener("DOMContentLoaded", () => {
  const tg = window.Telegram?.WebApp;
  const form = document.getElementById("requestForm");
  const result = document.getElementById("result");
  const resultContent = document.getElementById("resultContent");
  const copyButton = document.getElementById("copyBtn");
  const sendButton = document.getElementById("sendBtn");

  // Fail visibly instead of throwing an unclear error if HTML and JS drift apart.
  if (!form || !result || !resultContent || !copyButton || !sendButton) {
    console.error("Mini App page is missing required form/result elements.");
    return;
  }

  let currentPlan = "";
  if (tg) {
    tg.ready();
    tg.expand();
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const kind = document.getElementById("type").value.trim();
    const topic = document.getElementById("topic").value.trim();
    const subject = document.getElementById("subject").value.trim();
    const requirements = document.getElementById("requirements").value.trim();
    if (!topic || !subject) {
      form.reportValidity();
      return;
    }

    const sections = [
      ["Введение", `Объясните актуальность темы «${topic}», сформулируйте цель и задачи работы.`],
      ["1. Основные понятия", `Дайте определения ключевым понятиям по предмету «${subject}».`],
      ["2. Основная часть", `Раскройте тему «${topic}»: используйте проверенные факты, аргументы и примеры.`],
      ["Заключение", "Подведите итоги и кратко ответьте на задачи, поставленные во введении."],
      ["Источники", "Подберите реальные учебники и достоверные материалы; проверьте авторов, названия и даты публикации."]
    ];
    currentPlan = `${kind}: ${topic}\nПредмет: ${subject}\n\n` + sections.map(([title, text]) => `${title}\n${text}`).join("\n\n");
    if (requirements) currentPlan += `\n\nТребования преподавателя: ${requirements}`;
    currentPlan += "\n\nЭто план-заготовка, а не готовая академическая работа. Проверьте факты и требования преподавателя.";

    resultContent.replaceChildren();
    for (const [title, text] of sections) {
      const heading = document.createElement("h3");
      heading.textContent = title;
      const paragraph = document.createElement("p");
      paragraph.textContent = text;
      resultContent.append(heading, paragraph);
    }
    if (requirements) {
      const heading = document.createElement("h3");
      heading.textContent = "Требования преподавателя";
      const paragraph = document.createElement("p");
      paragraph.textContent = requirements;
      resultContent.append(heading, paragraph);
    }
    result.hidden = false;
    sendButton.textContent = "План подготовлен";
    result.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  copyButton.addEventListener("click", async () => {
    if (!currentPlan) return;
    try {
      await navigator.clipboard.writeText(currentPlan);
      copyButton.textContent = "Скопировано!";
      setTimeout(() => { copyButton.textContent = "Скопировать план"; }, 1800);
    } catch {
      copyButton.textContent = "Не удалось скопировать";
    }
  });
});
