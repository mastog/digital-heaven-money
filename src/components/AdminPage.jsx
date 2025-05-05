import React, { useState, useEffect, useRef } from 'react';
import ModalForm from './ModalForm.jsx';
import { apiRequest } from '../utils/api';
import '../styles/admin.css';
import modalStyles from "../utils/formConfigs/modal";

const RESOURCES = {
  DeceasedMessage: {
    name: 'Message',
    fields: ['id', 'message', 'deceased_id', 'user_id', 'posted_at'],
  },
  User: {
    name: 'User',
    fields: ['id', 'pic', 'username', 'email', 'gender', 'location', 'introduction', 'is_admin'],
  },
  Deceased: {
    name: 'Memorial',
    fields: [
      { name: 'id', type: 'hidden' },
      { name: 'pic', label: 'Picture', type: 'file', required: true },
      { name: 'name', label: 'Name', type: 'text', required: true },
      { name: 'birth_date', label: 'Birth Date', type: 'date', required: true },
      { name: 'death_date', label: 'Death Date', type: 'date', required: true },
      { name: 'biography', label: 'Description', type: 'textarea', required: true },
      { name: 'creator_id', type: 'hidden', value: 2},
      { name: 'created_at', type: 'hidden' },
    ],
  },
  DeceasedPhoto: {
    name: 'TimeLine',
    fields: [
      { name: 'id', type: 'hidden' },
      { name: 'pic', label: 'Picture', type: 'file', required: true },
      { name: 'title', label: 'Title', type: 'text', required: true },
      { name: 'photo_date', label: 'Time', type: 'month', required: true },
      { name: 'description', label: 'Description', type: 'textarea', required: true },
      { name: 'deceased_id', type: 'select', options: 'Deceased', required: true },
    ],
  },
  DeceasedUser: {
    name: 'Associated User',
    fields: ['id', 'deceased_id', 'user_id','joined_at'],
  },
};

const getFieldName = (field) => (typeof field === 'string' ? field : field.name);

const renderCellValue = (fieldName, item, onNavigateToResource) => {
  const value = item[fieldName];

  if (fieldName === 'pic' && item.pic_url) {
    return <img src={item.pic_url} alt="pic" className="h-16 w-16 object-cover rounded" />;
  }

  if (['deceased_id', 'user_id','creator_id'].includes(fieldName) && value) {
    return (
      <button
        onClick={() => onNavigateToResource(fieldName === 'deceased_id' ? 'Deceased' : 'User', value)}
        className="text-dark underline"
      >
        {fieldName.replace('_id', '')} #{value}
      </button>
    );
  }

  if (typeof value === 'boolean') {
    return value ? 'True' : 'False';
  } else if (value === null || value === undefined) {
    return '';
  } else {
    return value.toString();
  }
};

const AdminTable = ({
  resource,
  data,
  onRefresh,
  onNavigateToResource,
  highlightedId,
}) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  const rowRefs = useRef({});

  useEffect(() => {
    if (highlightedId && rowRefs.current[highlightedId]) {
      rowRefs.current[highlightedId].scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [highlightedId, data]);

  const handleDelete = async (id) => {
    await apiRequest(`/crud/${resource}/delete`, 'POST', { id });
    const {showNotification} = await import('../utils/notifications.js');
    showNotification(['Deletion successful']);
    await new Promise(resolve => setTimeout(resolve, 1000));
    window.location.reload();
  };

  const handleSort = (fieldName) => {
    let direction = 'asc';
    if (sortConfig.key === fieldName && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key: fieldName, direction });
    const sortedData = [...data].sort((a, b) => {
      const aValue = a[fieldName];
      const bValue = b[fieldName];
      if (aValue < bValue) return direction === 'asc' ? -1 : 1;
      if (aValue > bValue) return direction === 'asc' ? 1 : -1;
      return 0;
    });
    onRefresh(sortedData);
  };

  const showCreateButton = ['DeceasedPhoto', 'Deceased'].includes(resource);

  return (
    <div className="admin-panel">
      <div className="flex justify-between mb-4">
        <h2 className="text-xl font-bold">{RESOURCES[resource].name} Management</h2>
        {showCreateButton && (
            <ModalForm
              apiUrl={`/crud/${resource}/create`}
              method="POST"
              fields={RESOURCES[resource].fields}
              submitText="Submit"
              classConfig={modalStyles}
              onSuccess={async () => {
                window.location.reload();
              }}
            >
          <button className="btn-primary">
            Create {RESOURCES[resource].name}
          </button>
          </ModalForm>
        )}
      </div>

      <table className="w-full table-auto">
        <thead>
          <tr>
            {RESOURCES[resource].fields.map((field) => (
              <th key={getFieldName(field)} className="px-4 py-2 text-left">
                <button
                  onClick={() => handleSort(getFieldName(field))}
                  className="flex items-center gap-1 transform hover:scale-105"
                >
                  <span>{getFieldName(field)}</span>
                  {sortConfig.key === getFieldName(field) && (
                    <span>{sortConfig.direction === 'asc' ? '▲' : '▼'}</span>
                  )}
                </button>
              </th>
            ))}
            <th className="px-4 py-2">Operation</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => {
            const isHighlighted = item.id === highlightedId;
            return (
              <tr
                key={item.id}
                ref={(el) => (rowRefs.current[item.id] = el)}
                className={isHighlighted ? 'bg-yellow-100' : ''}
              >
                {RESOURCES[resource].fields.map((field) => {
                  const fieldName = getFieldName(field);
                  return (
                    <td
                      key={fieldName}
                      className={`border px-4 py-2 ${fieldName === 'pic' ? 'w-24' : ''}`}
                    >
                      {renderCellValue(fieldName, item, onNavigateToResource)}
                    </td>
                  );
                })}
                <td className="border px-4 py-2">
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="text-red-600 hover:text-red-800"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

const AdminPage = () => {
  const [selectedResource, setSelectedResource] = useState('User');
  const [tableData, setTableData] = useState([]);
  const [highlightedId, setHighlightedId] = useState(null);

  const loadData = async (resource) => {
    const response = (await apiRequest(`/crud/${resource}/get`, 'POST', {})) || [];
    setTableData(response);
  };

  useEffect(() => {
    loadData(selectedResource);
  }, [selectedResource]);

  const handleNavigateToResource = async (targetResource, idToHighlight) => {
    setSelectedResource(targetResource);
    setHighlightedId(null);
    const response = (await apiRequest(`/crud/${targetResource}/get`, 'POST', {})) || [];
    setTableData(response);
    setHighlightedId(idToHighlight);
  };

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="flex gap-4 mb-6">
        {Object.keys(RESOURCES).map((resource) => (
          <button
            key={resource}
            onClick={() => {
              setSelectedResource(resource);
              setHighlightedId(null);
            }}
            className={`px-4 py-2 rounded ${
              selectedResource === resource ? 'bg-dark text-white' : 'hover:bg-gray'
            }`}
          >
            {RESOURCES[resource].name}
          </button>
        ))}
      </div>

      {selectedResource && (
        <AdminTable
          resource={selectedResource}
          data={tableData}
          onRefresh={(newData) => setTableData(newData || tableData)}
          onNavigateToResource={handleNavigateToResource}
          highlightedId={highlightedId}
        />
      )}
    </div>
  );
};

export default AdminPage;
