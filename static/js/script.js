function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    fileInput.click();

    fileInput.onchange = function() {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
    
        // Mostrar tela de carregamento
        document.getElementById('loading').style.display = 'block';
    
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("opa")
                window.location.href = `download_file/${data.filename}`;
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        })
        .finally(() => { 
            // Ocultar tela de carregamento
            document.getElementById('loading').style.display = 'none';
        });
    };
}

function uploadFileProcessed() {
    const fileInput = document.getElementById('fileInput');
    fileInput.click();

    fileInput.onchange = function() {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
    
        // Mostrar tela de carregamento
        document.getElementById('loading').style.display = 'block';
    
        fetch('/upload_file_processed', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("opa")
                window.location.href = `download_file/${data.filename}`;
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        })
        .finally(() => { 
            // Ocultar tela de carregamento
            document.getElementById('loading').style.display = 'none';
        });
    };
}
