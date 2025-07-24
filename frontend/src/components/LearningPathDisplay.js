import React from "react";

function LearningPathDisplay({ learningPath }) {
  return (
    <div className="results">
      <h2>📚 Your Learning Path</h2>
      <ul>
        {learningPath.map((item, idx) => (
          <li key={idx}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default LearningPathDisplay;
