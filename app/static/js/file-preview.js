document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("file");
  const uploadContainer = document.querySelector(".upload-container");

  function formatFileSize(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
  }

  function formatDate(date) {
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    return `${day}/${month}/${year} às ${hours}:${minutes}`;
  }

  function createPreview(file) {
    const existingPreview = document.querySelector(".file-preview");

    if (existingPreview) {
      existingPreview.remove();
    }

    const extension = file.name.split(".").pop().toLowerCase();
    const size = formatFileSize(file.size);
    const lastModified = formatDate(new Date(file.lastModified));

    const previewHTML = `
      <div class="file-preview">
        <div class="file-preview-header">
          <span class="file-preview-title">Arquivo Selecionado</span>
          <button type="button" class="file-preview-close" aria-label="Remover arquivo">&times;</button>
        </div>
        <div class="file-preview-content">
          <div class="file-preview-info">
            <div class="file-preview-item">
              <span class="file-preview-label">Nome:</span>
              <span class="file-preview-value">${file.name}</span>
            </div>
            <div class="file-preview-item">
              <span class="file-preview-label">Tamanho:</span>
              <span class="file-preview-value">${size}</span>
            </div>
            <div class="file-preview-item">
              <span class="file-preview-label">Tipo:</span>
              <span class="file-preview-value">.${extension.toUpperCase()}</span>
            </div>
            <div class="file-preview-item">
              <span class="file-preview-label">Última modificação:</span>
              <span class="file-preview-value">${lastModified}</span>
            </div>
          </div>
        </div>
      </div>
    `;

    uploadContainer.insertAdjacentHTML("beforeend", previewHTML);

    const closeBtn = document.querySelector(".file-preview-close");

    closeBtn.addEventListener("click", function () {
      fileInput.value = "";
      document.querySelector(".file-preview").remove();
    });
  }

  fileInput.addEventListener("change", function (e) {
    if (this.files && this.files[0]) {
      createPreview(this.files[0]);
    }
  });

  uploadContainer.addEventListener("dragover", function (e) {
    e.preventDefault();
    this.classList.add("drag-over");
  });

  uploadContainer.addEventListener("dragleave", function (e) {
    e.preventDefault();
    this.classList.remove("drag-over");
  });

  uploadContainer.addEventListener("drop", function (e) {
    e.preventDefault();

    this.classList.remove("drag-over");

    const files = e.dataTransfer.files;

    if (files.length > 0) {
      const file = files[0];
      const extension = file.name.split(".").pop().toLowerCase();

      if (extension === "csv" || extension === "xlsx" || extension === "xls") {
        fileInput.files = files;
        createPreview(file);
      } else {
        console.error("Formato do arquivo diferente de .CSV ou .XLSX");
      }
    }
  });
});
