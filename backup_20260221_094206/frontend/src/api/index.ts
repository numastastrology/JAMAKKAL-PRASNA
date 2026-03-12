import axios from 'axios';
import type { PrasnaRequest, PrasnaResponse } from '../types';

const API_BASE_URL = 'http://localhost:8999';

export const calculatePrasna = async (data: PrasnaRequest): Promise<PrasnaResponse> => {
    const response = await axios.post(`${API_BASE_URL}/calculate`, data);
    return response.data;
};

export const downloadPDF = async (reportData: any) => {
    const response = await axios.post(`${API_BASE_URL}/generate-pdf`, reportData, {
        responseType: 'blob',
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `Prasna_Report_${new Date().getTime()}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
};
