import React from 'eact';
import RecipeItem from './RecipeItem';

const RecipeList = ({ recipes }) => {
  return (
    <ul>
      {recipes.map((recipe) => (
        <RecipeItem key={recipe.id} recipe={recipe} />
      ))}
    </ul>
  );
};

export default RecipeList;