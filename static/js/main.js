const data = {
    "Natural Sciences": ["Physics", "Chemistry", "Biology", "Mathematics", "Statistics", "Environmental Science", "Earth Science", "Astronomy", "Meteorology"],
    "Computer Science & IT": ["Computer Science", "Software Engineering", "Data Science", "Artificial Intelligence (AI)", "Machine Learning", "Cybersecurity", "Information Technology", "Web Development", "Cloud Computing", "Blockchain Technology"],
    "Engineering & Technology": ["Civil Engineering", "Mechanical Engineering", "Electrical Engineering", "Electronics Engineering", "Chemical Engineering", "Aerospace Engineering", "Biomedical Engineering", "Robotics", "Mechatronics", "Industrial Engineering", "Environmental Engineering", "Marine Engineering"],
    "Medical & Health Sciences": ["Medicine (MBBS)", "Nursing", "Dentistry", "Pharmacy", "Physiotherapy", "Radiology", "Public Health", "Nutrition & Dietetics", "Veterinary Science", "Psychology (Clinical)", "Biomedical Sciences"],
    "Business & Management": ["Business Administration (BBA/MBA)", "Finance", "Accounting", "Marketing", "Human Resource Management (HRM)", "Operations Management", "Entrepreneurship", "International Business", "Supply Chain Management"],
    "Social Sciences": ["Sociology", "Political Science", "Economics", "Anthropology", "History", "International Relations", "Social Work", "Development Studies"],
    "Humanities & Arts": ["Literature (English, French, etc.)", "Linguistics", "Philosophy", "Music", "Fine Arts", "Performing Arts (Dance, Theatre)", "History of Art", "Cultural Studies"],
    "Law & Legal Studies": ["Criminal Law", "Corporate Law", "Constitutional Law", "Intellectual Property Law", "International Law"],
    "Education": ["Primary Education", "Secondary Education", "Special Education", "Educational Technology", "Curriculum & Instruction"],
    "Agriculture & Allied Sciences": ["Agriculture", "Horticulture", "Forestry", "Animal Husbandry", "Fisheries Science", "Agronomy"],
    "Architecture & Design": ["Architecture", "Interior Design", "Urban Planning", "Graphic Design", "Fashion Design", "Product Design"],
    "Media & Communication": ["Journalism", "Mass Communication", "Digital Media", "Film Studies", "Advertising & PR"],
    "Emerging & Interdisciplinary Fields": ["Biotechnology", "Nanotechnology", "Renewable Energy", "Data Analytics", "Cognitive Science", "Bioinformatics", "Forensic Science", "Space Science"]
};

// Modal handling
const modal = document.getElementById('subjectsModal');
document.getElementById('openModalBtn').onclick = () => modal.style.display = 'block';
document.getElementById('closeModalBtn').onclick = () => modal.style.display = 'none';
window.onclick = e => { if (e.target === modal) modal.style.display = 'none'; };

const categoriesContainer = document.getElementById('categoriesContainer');
const searchInput = document.getElementById('searchInput');
const gradesField = document.getElementById('gradesField');

// Create checkbox with label
function createCheckbox(id, value, labelText) {
    const container = document.createElement('div');
    container.style.marginBottom = '5px';

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = id;
    checkbox.value = value;

    const label = document.createElement('label');
    label.htmlFor = id;
    label.textContent = labelText;
    label.style.marginLeft = '8px';

    container.appendChild(checkbox);
    container.appendChild(label);
    return container;
}

// Build the category list dynamically
function buildCategoryList() {
    categoriesContainer.innerHTML = '';
    Object.entries(data).forEach(([category, subjects]) => {
        const catDiv = document.createElement('div');
        catDiv.className = 'category';

        const catHeader = document.createElement('h3');
        catHeader.textContent = category;
        catDiv.appendChild(catHeader);

        const subjectsDiv = document.createElement('div');
        subjectsDiv.className = 'subjects-list';

        subjects.forEach((subject, idx) => {
            const safeCategory = category.replace(/[^a-zA-Z0-9]/g, '_');
            const checkboxId = `chk_${safeCategory}_${idx}`;
            subjectsDiv.appendChild(createCheckbox(checkboxId, subject, subject));
        });

        catDiv.appendChild(subjectsDiv);
        categoriesContainer.appendChild(catDiv);
    });
}

// Filter subjects by search input
function filterSubjects() {
    const filter = searchInput.value.toLowerCase();
    const categories = categoriesContainer.querySelectorAll('.category');

    categories.forEach(category => {
        let visibleCategory = false;
        const catName = category.querySelector('h3').textContent.toLowerCase();

        category.querySelectorAll('.subjects-list > div').forEach(div => {
            const labelText = div.querySelector('label').textContent.toLowerCase();
            const isVisible = labelText.includes(filter) || catName.includes(filter);
            div.style.display = isVisible ? '' : 'none';
            if (isVisible) visibleCategory = true;
        });

        category.style.display = visibleCategory ? '' : 'none';
    });
}

// Add selected subjects to grades field
function addSelectedSubjects() {
    const checked = categoriesContainer.querySelectorAll('input[type=checkbox]:checked');
    if (!checked.length) {
        alert('Please select at least one subject.');
        return;
    }

    let gradesMap = {};
    const currentGrades = gradesField.value.trim();

    if (currentGrades) {
        currentGrades.split(',').forEach(item => {
            let [subj, mark] = item.split(':').map(s => s.trim());
            if (subj) gradesMap[subj.toLowerCase()] = { subj, mark: mark || '0' };
        });
    }

    checked.forEach(cb => {
        const key = cb.value.toLowerCase();
        if (!gradesMap[key]) {
            gradesMap[key] = { subj: cb.value, mark: '0' };
        }
        cb.checked = false;
    });

    gradesField.value = Object.values(gradesMap).map(({ subj, mark }) => `${subj}: ${mark}`).join(', ');
    modal.style.display = 'none';
}

// Event bindings
window.onload = () => {
    buildCategoryList();
    searchInput.addEventListener('input', filterSubjects);
};
