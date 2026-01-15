async function summarizeText() {
    const inputText = document.getElementById("inputText").value;
    const loading = document.getElementById("loading");
    const summaryResult = document.getElementById("summaryResult");

    // Kiểm tra văn bản đầu vào
    if (!inputText) {
        summaryResult.innerHTML = "Error: Vui lòng nhập văn bản cần tóm tắt";
        return;
    }

    if (inputText.length > 1000) {
        summaryResult.innerHTML = "Error: Văn bản quá dài";
        return;
    }

    // Hiển thị loading
    loading.style.display = "block";
    summaryResult.innerHTML = "";

    try {
        console.log("Sending request with text:", inputText);
        const response = await fetch("http://127.0.0.1:5005/summarize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: inputText }),
        });

        console.log("Response status:", response.status);
        const data = await response.json();
        console.log("Response body:", data);

        if (response.ok) {
            summaryResult.innerHTML = `<strong>Summary:</strong> ${data.summary}`;
        } else {
            summaryResult.innerHTML = `Error: ${response.status} - ${JSON.stringify(data)}`;
        }
    } catch (error) {
        console.error("Error:", error);
        summaryResult.innerHTML = `Error: ${error.message}`;
    } finally {
        loading.style.display = "none";
    }
}