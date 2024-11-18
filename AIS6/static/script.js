// Функция для обработки удаления записи
function confirmDelete(recordId) {
    if (confirm("Вы уверены, что хотите удалить эту запись?")) {
        document.getElementById("delete_form_" + recordId).submit();
    }
}

// Динамическое добавление скрипта JavaScript в зависимости от статуса редактирования
function loadScript(editingEnabled) {
    if (!editingEnabled) {
        alert("Редактирование пока недоступно.");
    }
    
    // Обработчик нажатия на кнопки удаления записи
    if (editingEnabled) {
        var deleteButtons = document.querySelectorAll('.delete-button');
        deleteButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                var recordId = button.dataset.recordId;
                confirmDelete(recordId);
            });
        });
    }
}

// Получение значения editing_enabled из атрибута data-editing-enabled
var editingEnabled = document.querySelector('#editingEnabled').getAttribute('data-editing-enabled');

// Вызов функции для загрузки скрипта с передачей значения editingEnabled
loadScript(editingEnabled);
