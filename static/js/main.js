document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.url-form');
    const longUrlInput = document.getElementById('longUrl');
    const submitBtn = document.getElementById('submitBtn');
    const result = document.getElementById('result');
    const shortUrlInput = document.getElementById('shortUrl');
    const copyBtn = document.getElementById('copyBtn');

    submitBtn.addEventListener('click', async function() {
        const longUrl = longUrlInput.value;
        if (!longUrl) {
            alert('請輸入URL');
            return;
        }

        try {
            const response = await fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `url=${encodeURIComponent(longUrl)}`
            });
            const data = await response.json();
            
            if (data.error) {
                alert(data.error);
                return;
            }

            shortUrlInput.value = data.short_url;
            result.classList.remove('hidden');
        } catch (error) {
            alert('發生錯誤，請稍後再試');
        }
    });

    copyBtn.addEventListener('click', function() {
        shortUrlInput.select();
        document.execCommand('copy');
        copyBtn.textContent = '已複製！';
        setTimeout(() => {
            copyBtn.textContent = '複製';
        }, 2000);
    });
});
