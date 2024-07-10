import React, { useState } from 'eact';

const RecipeForm = () => {
  const [title, setTitle] = useState('');
  const [ingredients, setIngredients] = useState([]);
  const [steps, setSteps] = useState([]);
  const [cookingTime, setCookingTime] = useState('');
  const [servingSize, setServingSize] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Call API to create new recipe
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Title:
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
      </label>
      <label>
        Ingredients:
        <textarea value={ingredients} onChange={(e) => setIngredients(e.target.value.split(','))} />
      </label>
      <label>
        Steps:
        <textarea value={steps} onChange={(e) => setSteps(e.target.value.split(','))} />
      </label>
      <label>
        Cooking Time:
        <input type="text" value={cookingTime} onChange={(e) => setCookingTime(e.target.value)} />
      </label>
      <label>
        Serving Size:
        <input type="text" value={servingSize} onChange={(e) => setServingSize(e.target.value)} />
      </label>
      <button type="submit">Create Recipe</button>
    </form>
  );
};

export default RecipeForm;