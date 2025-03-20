export function getYiJiData(date) {
  // Simulate a 祭祀 data
  const data = {
  yi: [
    "Sacrifice", "Prayer for Blessing", "Marriage", "Wealth Acquisition",
    "Housewarming", "Starting a Business", "Signing a Contract", "Travel",
    "Building a House", "Relocation", "Seeking Medical Treatment", "Education",
    "Litigation", "Planting", "Purchasing Property", "Making Offerings",
    "Engagement", "Construction", "Hiring Employees", "Starting a New Job"
  ],
  ji: [
    "Groundbreaking", "Excavation", "Funeral", "Travel",
    "Starting a Business", "Signing a Contract", "Marriage", "Moving",
    "Litigation", "Climbing", "Visiting Friends", "Purchasing Property",
    "Making Offerings", "Engagement", "Construction", "Planting",
    "Hiring Employees", "Starting a New Job", "Education", "Seeking Medical Treatment"
  ]
};

  // random「宜」「忌」
  const yi = data.yi[Math.floor(Math.random() * data.yi.length)];
  const ji = data.ji[Math.floor(Math.random() * data.ji.length)];

  return { yi, ji };
}