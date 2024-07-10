import React from 'eact';

const RecipeItem = ({ recipe }) => {
  return (
    <li>
      <h2>{recipe.title}</h2>
      <p>Ingredients: {recipe.ingredients.join(', ')}</p>
      <p>Steps: {recipe.steps.join(', ')}</p>
      <p>Cooking Time: {recipe.cookingTime}</p>
      <p>Serving Size: {recipe.servingSize}</p>
    </li>
  );
};

export default RecipeItem;