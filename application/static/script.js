async function getRecommendations(event,skinType,tone) {
    try {
        event.preventDefault();  
        const selectedConcerns = Array.from(document.querySelectorAll('input[name="normal"]:checked, input[name="dry"]:checked, input[name="oily"]:checked, input[name="combination"]:checked, input[name="acne"]:checked, input[name="sensitive"]:checked, input[name="fine lines"]:checked, input[name="wrinkles"]:checked, input[name="redness"]:checked, input[name="dull"]:checked, input[name="pore"]:checked, input[name="pigmentation"]:checked, input[name="blackheads"]:checked, input[name="whiteheads"]:checked, input[name="blemishes"]:checked, input[name="dark circles"]:checked, input[name="eye bags"]:checked, input[name="dark spots"]:checked')).map(checkbox => checkbox.name);
        console.log(selectedConcerns)
        const features = {
            normal: selectedConcerns.includes('normal') ? 1 : 0,
            dry: selectedConcerns.includes('dry') ? 1 : 0,
            oily: selectedConcerns.includes('oily') ? 1 : 0,
            combination: selectedConcerns.includes('combination') ? 1 : 0,
            acne: selectedConcerns.includes('acne') ? 1 : 0,
            sensitive: selectedConcerns.includes('sensitive') ? 1 : 0,
            "fine lines": selectedConcerns.includes('fine lines') ? 1 : 0,
            wrinkles: selectedConcerns.includes('wrinkles') ? 1 : 0,
            redness: selectedConcerns.includes('redness') ? 1 : 0,
            dull: selectedConcerns.includes('dull') ? 1 : 0,
            pore: selectedConcerns.includes('pore') ? 1 : 0,
            pigmentation: selectedConcerns.includes('pigmentation') ? 1 : 0,
            blackheads: selectedConcerns.includes('blackheads') ? 1 : 0,
            whiteheads: selectedConcerns.includes('whiteheads') ? 1 : 0,
            blemishes: selectedConcerns.includes('blemishes') ? 1 : 0,
            "dark circles": selectedConcerns.includes('dark circles') ? 1 : 0,
            "eye bags": selectedConcerns.includes('eye bags') ? 1 : 0,
            "dark spots": selectedConcerns.includes('dark spots') ? 1 : 0,
        };

        const response = await fetch('/recommend', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tone: parseInt(tone),  // Assuming you have a default value for tone
                type: skinType,  // Assuming you have a default value for skin type
                features: features,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

       

        const generalRecommendations = data.general;
        if (generalRecommendations) {
            displayRecommendations(generalRecommendations, 'skincare-recommendations');
        }

        const makeupRecommendations = data.makeup;
        
        if (makeupRecommendations != null) {
            displayMakeupRecommendations(makeupRecommendations, 'makeup-recommendations');
        }

    } catch (error) {
        console.error('Error fetching recommendations:', error);
        // document.getElementById('recommendation-results').innerHTML = "<p>Error fetching recommendations. Please try again later.</p>";
    }
}

function displayRecommendations(recommendations, elementId) {
    const recommendationResults = document.getElementById(elementId);
    recommendationResults.innerHTML += "<h1>Skincare Recommendations</h1>";

    if(recommendationResults != null){
        for (const category in recommendations) {
            if (recommendations.hasOwnProperty(category) && recommendations[category].length > 0) {
                // Create a section for each category
                const categorySection = document.createElement('div');
                categorySection.className = 'category-section';
    
                // Add a heading for the category
                const categoryHeading = document.createElement('h3');
                categoryHeading.textContent = category.charAt(0).toUpperCase() + category.slice(1); // Capitalize the first letter
                categorySection.appendChild(categoryHeading);
    
                // Create a container for items in the category
                const categoryContainer = document.createElement('div');
                categoryContainer.className = 'category-container';
    
                recommendations[category].forEach(item => {
                    // Create an item for each recommendation
                    const itemContainer = document.createElement('div');
                    itemContainer.className = 'makeup-item';
    
                    const img = document.createElement('img');
                    img.src = item.img;
                    img.alt = `${item.brand} - ${item.name}`;
    
                    const brandName = document.createElement('strong');
                    brandName.textContent = item.brand;
    
                    const productName = document.createElement('span');
                    productName.textContent = item.name;
    
                    const price = document.createElement('span');
                    price.textContent = `Price: ${item.price}`;
    
                    const concern = document.createElement('span');
                    concern.textContent = `Concerns: ${item.concern.join(', ')}`;
    
                    const link = document.createElement('a');
                    link.href = item.url;
                    link.textContent = 'View on Myntra';
    
                    itemContainer.appendChild(img);
                    itemContainer.appendChild(brandName);
                    itemContainer.appendChild(productName);
                    itemContainer.appendChild(price);
                    itemContainer.appendChild(concern);
                    itemContainer.appendChild(link);
    
                    categoryContainer.appendChild(itemContainer);
                });
    
                categorySection.appendChild(categoryContainer);
                recommendationResults.appendChild(categorySection);
            }
        }
    }
    
}

function displayMakeupRecommendations(recommendations, elementId) {
    const recommendationResults = document.getElementById(elementId);    
    
    if(recommendationResults != null){            
        recommendationResults.innerHTML += "<h1>Makeup Recommendations</h1>";
        // Create a container for items in the category
        const categoryContainer = document.createElement('div');
        categoryContainer.className = 'category-container';
        recommendations.forEach(item => {
            // Create an item for each recommendation
            const itemContainer = document.createElement('div');
            itemContainer.className = 'makeup-item';

            const img = document.createElement('img');
            img.src = item.img;
            img.alt = `${item.brand} - ${item.name}`;

            const brandName = document.createElement('strong');
            brandName.textContent = item.brand;

            const productName = document.createElement('span');
            productName.textContent = item.name;

            const price = document.createElement('span');
            price.textContent = `Price: ${item.price}`;

            const concern = document.createElement('span');
            concern.textContent = `Concerns: ${item.concern ? item.concern.join(', ') : 'N/A'}`;

            const link = document.createElement('a');
            link.href = item.url;
            link.textContent = 'View on Myntra';

            itemContainer.appendChild(img);
            itemContainer.appendChild(brandName);
            itemContainer.appendChild(productName);
            itemContainer.appendChild(price);
            itemContainer.appendChild(concern);
            itemContainer.appendChild(link);

            categoryContainer.appendChild(itemContainer);
        });  
        recommendationResults.appendChild(categoryContainer);
 
    
    }      
    
}
