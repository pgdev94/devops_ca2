const form = document.getElementById("feedbackForm");
const messageBox = document.getElementById("formMessage");

const fields = {
  studentName: document.getElementById("studentName"),
  email: document.getElementById("email"),
  mobile: document.getElementById("mobile"),
  department: document.getElementById("department"),
  feedback: document.getElementById("feedback")
};

const errors = {
  studentName: document.getElementById("studentNameError"),
  email: document.getElementById("emailError"),
  mobile: document.getElementById("mobileError"),
  department: document.getElementById("departmentError"),
  gender: document.getElementById("genderError"),
  feedback: document.getElementById("feedbackError")
};

function setError(field, text) {
  errors[field].textContent = text;
}

function clearErrors() {
  Object.values(errors).forEach((el) => {
    el.textContent = "";
  });
}

function clearMessage() {
  messageBox.textContent = "";
  messageBox.className = "message";
}

function wordCount(text) {
  return text
    .trim()
    .split(/\s+/)
    .filter(Boolean).length;
}

function validateName() {
  const value = fields.studentName.value.trim();
  if (!value) {
    setError("studentName", "Student Name is required.");
    return false;
  }
  setError("studentName", "");
  return true;
}

function validateEmail() {
  const value = fields.email.value.trim();
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  if (!value) {
    setError("email", "Email ID is required.");
    return false;
  }
  if (!emailRegex.test(value)) {
    setError("email", "Enter a valid email format.");
    return false;
  }
  setError("email", "");
  return true;
}

function validateMobile() {
  const value = fields.mobile.value.trim();
  const mobileRegex = /^\d{10}$/;
  if (!value) {
    setError("mobile", "Mobile Number is required.");
    return false;
  }
  if (!mobileRegex.test(value)) {
    setError("mobile", "Mobile Number must contain exactly 10 digits.");
    return false;
  }
  setError("mobile", "");
  return true;
}

function validateDepartment() {
  if (!fields.department.value) {
    setError("department", "Please select a department.");
    return false;
  }
  setError("department", "");
  return true;
}

function validateGender() {
  const selected = document.querySelector('input[name="gender"]:checked');
  if (!selected) {
    setError("gender", "Please select a gender option.");
    return false;
  }
  setError("gender", "");
  return true;
}

function validateFeedback() {
  const value = fields.feedback.value.trim();
  if (!value) {
    setError("feedback", "Feedback Comments cannot be blank.");
    return false;
  }
  if (wordCount(value) < 10) {
    setError("feedback", "Feedback must contain at least 10 words.");
    return false;
  }
  setError("feedback", "");
  return true;
}

function validateForm() {
  return [
    validateName(),
    validateEmail(),
    validateMobile(),
    validateDepartment(),
    validateGender(),
    validateFeedback()
  ].every(Boolean);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  clearMessage();
  clearErrors();

  if (validateForm()) {
    messageBox.textContent = "Feedback submitted successfully.";
    messageBox.classList.add("success");
    return;
  }

  messageBox.textContent = "Please correct the highlighted errors and submit again.";
  messageBox.classList.add("error");
});

form.addEventListener("reset", () => {
  // Reset happens immediately after this event, so clear messages on next tick.
  setTimeout(() => {
    clearErrors();
    clearMessage();
  }, 0);
});
