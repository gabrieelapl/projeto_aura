const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');

// Efeito de hover e clique
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// Atualizar informações do arquivo selecionado
fileInput.addEventListener('change', function() {
    if (this.files.length > 0) {
        fileName.textContent = this.files[0].name;
        fileInfo.classList.add('show');
        
        // Efeito visual de confirmação
        uploadArea.style.borderColor = '#2ecc71';
        uploadArea.style.backgroundColor = '#f0fff4';
        
        setTimeout(() => {
            uploadArea.style.borderColor = '';
            uploadArea.style.backgroundColor = '';
        }, 1000);
    }
});

// Suporte para arrastar e soltar
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#3498db';
    uploadArea.style.backgroundColor = '#e8f4fc';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = '';
    uploadArea.style.backgroundColor = '';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '';
    uploadArea.style.backgroundColor = '';
    
    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        fileName.textContent = e.dataTransfer.files[0].name;
        fileInfo.classList.add('show');
        
        // Efeito visual de confirmação
        uploadArea.style.borderColor = '#2ecc71';
        uploadArea.style.backgroundColor = '#f0fff4';
        
        setTimeout(() => {
            uploadArea.style.borderColor = '';
            uploadArea.style.backgroundColor = '';
        }, 1000);
    }
});