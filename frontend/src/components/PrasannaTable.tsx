import React from 'react';
import type { PrasannaSpecial } from '../types';

interface PrasannaTableProps {
    data: PrasannaSpecial;
}

const formatPerc = (val: number) => {
    return val.toFixed(2) + '%';
};

export const PrasannaTable: React.FC<PrasannaTableProps> = ({ data }) => {
    if (!data) return null;

    return (
        <div className="mt-8 bg-[#FFDDC1] rounded-lg shadow-xl overflow-hidden self-center max-w-lg mx-auto border-2 border-[#ECA06F]">
            {/* Header */}
            <div className="bg-[#FFDDC1] py-4 text-center border-b border-[#ECA06F]">
                <h3 className="text-xl font-bold text-black tracking-wide font-sans">
                    Prasanna Details Special
                </h3>
            </div>

            {/* Table Area */}
            <div className="flex flex-col bg-[#FFFAF0]">
                {/* Row 1 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F]">
                    <div className="text-gray-800 text-sm md:text-base">
                        <div>Planet Towards</div>
                        <div>Udhayam</div>
                    </div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        <div>{data.udhayam.planet}</div>
                        <div>{formatPerc(data.udhayam.percent)}</div>
                    </div>
                </div>

                {/* Row 2 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F] bg-[#FFF3E0]">
                    <div className="text-gray-800 text-sm md:text-base">
                        <div>Udhayam Lord and its</div>
                        <div>Bhava</div>
                    </div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        <div>{data.udhayam_lord.planet}</div>
                        <div>- {data.udhayam_lord.bhava}</div>
                    </div>
                </div>

                {/* Row 3 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F]">
                    <div className="text-gray-800 text-sm md:text-base">Arudam Bhava</div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        {data.arudam_bhava}
                    </div>
                </div>

                {/* Row 4 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F] bg-[#FFF3E0]">
                    <div className="text-gray-800 text-sm md:text-base">Planet towards Arudam</div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        <div>{data.arudam.planet}</div>
                        <div>{formatPerc(data.arudam.percent)}</div>
                    </div>
                </div>

                {/* Row 5 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F]">
                    <div className="text-gray-800 text-sm md:text-base">Planet towards Kavipu</div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        <div>{data.kavipu.planet}</div>
                        <div>{formatPerc(data.kavipu.percent)}</div>
                    </div>
                </div>

                {/* Row 6 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F] bg-[#FFF3E0]">
                    <div className="text-gray-800 text-sm md:text-base">Bhava in Kavipu</div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        {data.kavipu_bhava}
                    </div>
                </div>

                {/* Row 7 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F]">
                    <div className="text-gray-800 text-sm md:text-base">Exalted Planets</div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        {data.exalted.length > 0 ? data.exalted.join(', ') + ',' : ''}
                    </div>
                </div>

                {/* Row 8 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F] bg-[#FFF3E0]">
                    <div className="text-gray-800 text-sm md:text-base">Debilitated Planets</div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        {data.debilitated.length > 0 ? data.debilitated.join(', ') + ',' : ''}
                    </div>
                </div>

                {/* Row 9 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F]">
                    <div className="text-gray-800 text-sm md:text-base">Parivarthana Planets</div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        {data.parivarthana.length > 0 ? data.parivarthana.join(', ') + ',' : ''}
                    </div>
                </div>

                {/* Row 10 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F] bg-[#FFF3E0]">
                    <div className="text-gray-800 text-sm md:text-base">Kuligan Bhava</div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        {data.kuligan_bhava}
                    </div>
                </div>

                {/* Row 11 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F]">
                    <div className="text-gray-800 text-sm md:text-base">Planet towards Kuligan</div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        <div>{data.kuligan.planet}</div>
                        <div>{formatPerc(data.kuligan.percent)}</div>
                    </div>
                </div>

                {/* Row 12 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F] bg-[#FFF3E0]">
                    <div className="text-gray-800 text-sm md:text-base">
                        <div>Planet towards</div>
                        <div>Emakandam</div>
                    </div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        <div>{data.emakandam.planet}</div>
                        <div>{formatPerc(data.emakandam.percent)}</div>
                    </div>
                </div>

                {/* Row 13 */}
                <div className="flex justify-between py-3 px-6 border-b border-[#ECA06F]">
                    <div className="text-gray-800 text-sm md:text-base">
                        <div>Planet towards Rahu</div>
                        <div>Time</div>
                    </div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        <div>{data.rahu_time.planet}</div>
                        <div>{formatPerc(data.rahu_time.percent)}</div>
                    </div>
                </div>

                {/* Row 14 */}
                <div className="flex justify-between py-3 px-6 bg-[#FFF3E0]">
                    <div className="text-gray-800 text-sm md:text-base">Planet towards Mrithyu</div>
                    <div className="text-right text-[#C92A2A] text-sm md:text-base font-semibold">
                        <div>{data.mrithyu.planet}</div>
                        <div>{formatPerc(data.mrithyu.percent)}</div>
                    </div>
                </div>
            </div>
        </div>
    );
};
