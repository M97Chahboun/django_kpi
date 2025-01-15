document.addEventListener("DOMContentLoaded", function () {
  // Cache DOM elements with null checks
  const modelField = document.getElementById("id_kpi");
  const targetField = document.getElementById("id_target_field");
  let targetValue = document.getElementById("id_target_value"); // Using let since we reassign it
  const condition = document.getElementById("id_condition");
  const targetType = document.getElementById("id_target_type");
  const csrfTokenElement = document.querySelector(
    '[name="csrfmiddlewaretoken"]'
  );
  const targetValueForm = document.querySelector(".field-target_value");

  // Verify that all required elements exist
  if (
    !modelField ||
    !targetField ||
    !targetValue ||
    !condition ||
    !targetType ||
    !targetValueForm
  ) {
    console.error(
      "Required form elements are missing. Please check the HTML structure."
    );
    return; // Exit if required elements are missing
  }

  // Get CSRF token with null check
  const csrfToken = csrfTokenElement ? csrfTokenElement.value : "";

  // Setup fetch headers with CSRF token
  const headers = {
    "X-CSRFToken": csrfToken,
    "Content-Type": "application/json",
  };

  // Convert target value to select element
  function convertToSelect() {
    if (!targetValue) return;

    if (targetValue.tagName.toLowerCase() !== "select") {
      try {
        const attributes = getAttributes(targetValue);
        const select = document.createElement("select");
        Object.keys(attributes).forEach((attr) => {
          select.setAttribute(attr, attributes[attr]);
        });

        if (targetValue.parentNode) {
          targetValue.parentNode.replaceChild(select, targetValue);
          targetValue = select; // Update the reference
        }
      } catch (error) {
        console.error("Error converting to select:", error);
      }
    }
  }

  // Convert target value to text field
  function updateToTextField() {
    if (!targetValue) return;

    if (targetValue.tagName.toLowerCase() !== "input") {
      try {
        const attributes = getAttributes(targetValue);
        const input = document.createElement("input");
        const value = targetValue.value;

        Object.keys(attributes).forEach((attr) => {
          input.setAttribute(attr, attributes[attr]);
        });
        input.type = "text";
        input.value = value;

        if (targetValue.parentNode) {
          targetValue.parentNode.replaceChild(input, targetValue);
          targetValue = input; // Update the reference
        }
      } catch (error) {
        console.error("Error converting to text field:", error);
      }
    }
  }

  // Toggle target value field based on condition
  function toggleTargetValueField() {
    if (!condition || !targetValue || !targetValueForm) return;

    const conditionValue = condition.value;
    const fromEl = document.getElementById("from");
    const toEl = document.getElementById("to");

    // Safely remove elements if they exist
    if (fromEl) fromEl.remove();
    if (toEl) toEl.remove();

    if (conditionValue === "NONE") {
      targetValueForm.style.display = "none";
    } else {
      targetValueForm.style.display = "";
      targetValue.style.display = "";

      try {
        if (conditionValue.includes("EXACT")) {
          updateFieldValues();
          convertToSelect();
        } else if (conditionValue === "BETWEEN") {
          updateToTextField();
          setupBetweenFields();
        } else {
          updateToTextField();
        }
      } catch (error) {
        console.error("Error in toggleTargetValueField:", error);
      }
    }
  }

  // Setup 'between' fields
  function setupBetweenFields() {
    if (!targetValue || !targetValue.parentNode) return;

    try {
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
    } catch (error) {
      console.error("Error in setupBetweenFields:", error);
    }
  }

  // Get attributes of an element
  function getAttributes(element, justClass = false) {
    if (!element || !element.attributes) return {};

    const attributes = {};
    Array.from(element.attributes).forEach((attr) => {
      if (!justClass || attr.name === "class") {
        attributes[attr.name] = attr.value;
      }
    });
    return attributes;
  }

  // Update field values based on selected model and field
  function updateFieldValues() {
    if (!modelField || !targetField || !targetValue) return;

    const modelName = modelField.options[modelField.selectedIndex]?.text;
    const fieldName = targetField.value;
    const fieldType =
      targetField.options[targetField.selectedIndex]?.dataset.type;

    if (targetType) {
      targetType.value = fieldType || "";
    }

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

  // Initialize event listeners only if elements exist
  if (modelField) {
    modelField.addEventListener("change", updateModelFields);
  }
  if (targetField) {
    targetField.addEventListener("change", updateFieldValues);
  }
  if (condition) {
    condition.addEventListener("change", toggleTargetValueField);
  }

  // Initialize if all required elements exist
  if (modelField && targetField && targetValue && condition) {
    toggleTargetValueField();

    // If editing, store initial values and trigger updates
    if (modelField.value) {
      window.initialTargetField = targetField.value;
      window.initialTargetValue = targetValue.value;
      updateModelFields();
    }
  }

  // Update model fields based on selected model
  function updateModelFields() {
    if (!modelField || !targetField) return;

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

        targetField.innerHTML = '<option value="">-- Select Field --</option>';

        response.fields.forEach((field) => {
          const option = document.createElement("option");
          option.value = field.name;
          option.textContent = field.verbose_name;
          option.dataset.type = field.type;
          targetField.appendChild(option);
        });

        if (window.initialTargetField) {
          targetField.value = window.initialTargetField;
          updateFieldValues();
        }
      })
      .catch((error) => console.error("Fetch Error:", error));
  }
});
