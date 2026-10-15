import React, { useState } from "react";

export default function Register() {
  const [form, setForm] = useState({
    username: "",
    firstName: "",
    lastName: "",
    email: "",
    password: ""
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Sign-up form submitted successfully!");
  };

  const inputStyle = {
    display: "block",
    width: "100%",
    padding: "10px",
    marginTop: "6px",
    marginBottom: "16px",
    boxSizing: "border-box",
    border: "1px solid #ccc",
    borderRadius: "5px"
  };

  return (
    <div style={{
      maxWidth: "420px",
      margin: "40px auto",
      padding: "28px",
      fontFamily: "Arial, sans-serif",
      border: "1px solid #ddd",
      borderRadius: "10px"
    }}>
      <h2 style={{ textAlign: "center" }}>Sign-up</h2>
      <form onSubmit={handleSubmit}>
        <label>Username</label>
        <input style={inputStyle} name="username" value={form.username}
          onChange={handleChange} required />

        <label>First Name</label>
        <input style={inputStyle} name="firstName" value={form.firstName}
          onChange={handleChange} required />

        <label>Last Name</label>
        <input style={inputStyle} name="lastName" value={form.lastName}
          onChange={handleChange} required />

        <label>Email</label>
        <input style={inputStyle} type="email" name="email" value={form.email}
          onChange={handleChange} required />

        <label>Password</label>
        <input style={inputStyle} type="password" name="password"
          value={form.password} onChange={handleChange} required />

        <button type="submit" style={{
          width: "100%",
          padding: "12px",
          background: "#1769aa",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer"
        }}>
          Register
        </button>
      </form>
    </div>
  );
}
