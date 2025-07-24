const BASE_URL = "http://localhost:8000";

export async function generateLearningPath(userGoal, secondaryTool) {
  const response = await fetch(`${BASE_URL}/generate-learning-path`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_goal: userGoal, secondary_tool: secondaryTool })
  });
  return await response.json();
}
