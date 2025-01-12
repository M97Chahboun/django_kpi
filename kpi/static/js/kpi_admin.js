document.addEventListener("DOMContentLoaded", function () {
  // Cache DOM elements
  const modelField = document.getElementById("id_kpi");
  const targetField = document.getElementById("id_target_field");
  const targetValue = document.getElementById("id_target_value");
  const condition = document.getElementById("id_condition");
  const targetType = document.getElementById("id_target_type");
  const csrfToken = document.querySelector(
    '[name="csrfmiddlewaretoken"]'
  ).value;
  const targetValueForm = document.querySelector(".field-target_value");

  // Setup fetch headers with CSRF token
  const headers = {
    "X-CSRFToken": csrfToken,
    "Content-Type": "application/json",
  };

  // Update model fields based on selected model
  function updateModelFields() {
    const modelName = modelField.options[modelField.selectedIndex]?.text;
    if (!modelName) return;

    fetch(`/kpi/get-model-fields/?model=${encodeURIComponent(modelName)}`, {
      method: "GET",
      headers: headers,
    })
      .then((response) => response.json())
      .then((response) => {
        if (response.error) {
          console.error("Error:", response.error);
          return;
        }

        // Clear and update target field select options
        targetField.innerHTML = '<option value="">-- Select Field --</option>';

        response.fields.forEach((field) => {
          const option = document.createElement("option");
          option.value = field.name;
          option.textContent = field.verbose_name;
          option.dataset.type = field.type;
          targetField.appendChild(option);
        });

        // Restore previous selection if editing
        if (window.initialTargetField) {
          targetField.value = window.initialTargetField;
          updateFieldValues(); // Trigger value update
        }
      })
      .catch((error) => console.error("Fetch Error:", error));
  }

  // Toggle target value field based on condition
  function toggleTargetValueField() {
    const conditionValue = condition.value;
    const fromEl = document.getElementById("from");
    const toEl = document.getElementById("to");

    if (fromEl) fromEl.remove();
    if (toEl) toEl.remove();

    if (conditionValue === "NONE") {
      targetValueForm.style.display = "none";
    } else {
      targetValueForm.style.display = "";
      targetValue.style.display = "";

      if (conditionValue.includes("EXACT")) {
        updateFieldValues();
        convertToSelect();
      } else if (conditionValue === "BETWEEN") {
        updateToTextField();
        setupBetweenFields();
      } else {
        updateToTextField();
      }
    }
  }

  // Convert target value to select element
  function convertToSelect() {
    if (targetValue.tagName.toLowerCase() !== "select") {
      const attributes = getAttributes(targetValue);
      const select = document.createElement("select");
      Object.keys(attributes).forEach((attr) => {
        select.setAttribute(attr, attributes[attr]);
      });
      targetValue.parentNode.replaceChild(select, targetValue);
      targetValue = select;
    }
  }

  // Convert target value to text field
  function updateToTextField() {
    if (targetValue.tagName.toLowerCase() !== "input") {
      const attributes = getAttributes(targetValue);
      const input = document.createElement("input");
      const value = targetValue.value;

      Object.keys(attributes).forEach((attr) => {
        input.setAttribute(attr, attributes[attr]);
      });
      input.type = "text";
      input.value = value;

      targetValue.parentNode.replaceChild(input, targetValue);
      targetValue = input;
    }
  }

  // Setup 'between' fields
  function setupBetweenFields() {
    const attributes = getAttributes(targetValue, true);
    let fromInput = document.getElementById("from");
    let toInput = document.getElementById("to");

    if (!fromInput) {
      fromInput = document.createElement("input");
      fromInput.type = "text";
      fromInput.id = "from";
      fromInput.placeholder = "from";
      fromInput.style.margin = "5px";
      Object.keys(attributes).forEach((attr) => {
        fromInput.setAttribute(attr, attributes[attr]);
      });
      targetValue.parentNode.appendChild(fromInput);
    }

    if (!toInput) {
      toInput = document.createElement("input");
      toInput.type = "text";
      toInput.id = "to";
      toInput.placeholder = "to";
      toInput.style.margin = "5px";
      Object.keys(attributes).forEach((attr) => {
        toInput.setAttribute(attr, attributes[attr]);
      });
      targetValue.parentNode.appendChild(toInput);
    }

    targetValue.style.display = "none";
    const values = targetValue.value.split(" to ");
    if (values.length === 2) {
      fromInput.value = values[0];
      toInput.value = values[1];
    }

    const updateTargetValue = () => {
      targetValue.value = `${fromInput.value} to ${toInput.value}`;
    };

    fromInput.addEventListener("input", updateTargetValue);
    toInput.addEventListener("input", updateTargetValue);
  }

  // Update field values based on selected model and field
  function updateFieldValues() {
    const modelName = modelField.options[modelField.selectedIndex]?.text;
    const fieldName = targetField.value;
    const fieldType =
      targetField.options[targetField.selectedIndex]?.dataset.type;

    targetType.value = fieldType;
    if (!modelName || !fieldName) return;

    fetch(
      `/kpi/get-field-values/?model=${encodeURIComponent(
        modelName
      )}&field=${encodeURIComponent(fieldName)}`,
      {
        method: "GET",
        headers: headers,
      }
    )
      .then((response) => response.json())
      .then((response) => {
        if (response.error) {
          console.error("Error:", response.error);
          return;
        }

        const currentValue = targetValue.value;
        targetValue.innerHTML = '<option value="">-- Select Value --</option>';

        response.values.forEach((value) => {
          const option = document.createElement("option");
          option.value = value;
          option.textContent = value;
          if (value === currentValue) {
            option.selected = true;
          }
          targetValue.appendChild(option);
        });
      })
      .catch((error) => console.error("Fetch Error:", error));
  }

  // Get attributes of an element
  function getAttributes(element, justClass = false) {
    const attributes = {};
    Array.from(element.attributes).forEach((attr) => {
      if (!justClass || attr.name === "class") {
        attributes[attr.name] = attr.value;
      }
    });
    return attributes;
  }

  // Event listeners
  modelField.addEventListener("change", updateModelFields);
  targetField.addEventListener("change", updateFieldValues);
  condition.addEventListener("change", toggleTargetValueField);

  // Initialize
  toggleTargetValueField();

  // If editing, store initial values and trigger updates
  if (modelField.value) {
    window.initialTargetField = targetField.value;
    window.initialTargetValue = targetValue.value;
    updateModelFields();
  }
});
