from itertools import chain
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

np.random.seed(42)

s = "7D81_A_NAD_104	2HO6_A_MES_401	2HO6_B_MES_402	4OQU_A_SAM_101	6CK4_A_GTP_201	6CK4_A_G4P_214	6CK4_B_G4P_208	6CK4_C_G4P_211	6CK4_D_G4P_211	3DVV_A_RIO_27	3DVV_B_RIO_26	1JZY_A_ERY_2881	4V74_BA_FME_3001	5MDW_5_FME_101	7M4Y_a_YQM_1601	7D7Y_A_ATP_102	3CXC_0_SLD_9500	7NSI_AA_SPM_3001	7NSI_BA_5GP_1792	7NSI_BA_SPM_1793	3T1Y_A_PAR_1786	6HIY_CA_SPM_735	4LX6_A_29H_601	6WDI_5_FME_101	6YMI_A_CBV_101	6YMI_A_AMP_102	6YMI_A_AMP_103	6YMI_C_CBV_101	6YMI_C_AMP_102	6YMI_F_CBV_101	6YMI_F_AMP_102	6YMI_G_AMP_101	6YMI_I_CBV_101	6YMI_I_AMP_102	6YMI_M_CBV_101	6YMI_M_AMP_102	6YMI_N_AMP_101	6YMI_O_CBV_101	6YMI_O_AMP_102	7N2U_23_ATP_3001	5T83_A_SPK_110	1AJU_A_ARG_47	6O97_1A_LUJ_4099	6O97_1A_LUJ_4100	6O97_1a_LUJ_1832	6O97_2A_LUJ_3851	6O97_2A_LUJ_3852	6O97_2a_LUJ_3232	6DME_A_G4P_201	1YJN_0_CLY_9000	4LSK_QA_PAR_1666	4LSK_XA_PAR_1675	3MUV_R_2BA_358	7MT2_y_FME_101	7D7W_A_GTP_101	7D7W_A_NAD_102	5FK5_A_SAM_1095	2OE8_B_AM2_101	1NEM_A_BDG_27	1NEM_A_NEB_28	4E8M_A_SPM_443	4E8M_A_SPM_444	6HIW_CA_SPM_740	6WDG_7_PHE_101	6WDG_7_FME_102	7TDB_A_GMI_101	3GX7_A_SAM_301	1M1K_A_ZIT_8600	5WNU_A_B6M_1858	1IBK_A_PAR_1545	5XZ1_A_GET_101	5XZ1_B_GET_301	5XZ1_C_GET_101	5XZ1_C_GET_102	6ND6_1A_ERY_4074	6ND6_2A_ERY_3875	3WRU_A_SJP_101	3WRU_B_SJP_101	4GPX_A_6HS_101	4GPX_B_6HS_101	3F4G_Y_RBF_200	1TN1_A_SPM_77	5UYL_W_FME_101	6Y2L_L5_3HE_5101	1IBL_A_PAR_1545	1HNW_A_TAC_1633	6YWE_A_SPM_3636	7M4W_a_YQM_1601	3JBV_b_CLM_9000	5MDY_5_FME_103	5FK2_A_SAM_1095	2FCZ_A_RIO_1024	2FCZ_B_RIO_2024	2FCZ_C_RIO_3024	2FCZ_D_RIO_4024	2ET5_A_RIO_54	2ET5_B_RIO_51	2ET5_B_RIO_52	2ET5_B_RIO_53	6YPU_4_AKN_1607	5WE4_v_FME_101	4P3S_A_GET_101	4P3S_A_GET_102	4P3S_A_GET_103	6DB8_R_G4A_101	6JJH_B_POH_101	6XRQ_A_V8A_102	6XRQ_A_V8A_103	1EHT_A_TEP_34	4QK9_A_2BA_201	4QK9_A_2BA_202	4E8Q_A_SPM_448	4LF4_A_LLL_1749	5FCJ_1_ANM_3401	2PWT_A_LHA_51	2PWT_B_LHA_50	6LAU_A_SAH_101	6LAU_A_GTP_103	6LAU_B_SAH_101	3NPQ_A_SAH_55	3NPQ_B_SAH_55	3NPQ_C_SAH_55	5IQR_2_PAR_1665	5DGE_1_SPS_4113	5DGE_5_SPS_3403	4V6Q_BB_FME_3001	4YBB_AA_PG4_1670	4YBB_BA_PG4_1642	4YBB_DA_1PE_3185	4YBB_DA_PG4_3193	4YBB_DA_1PE_3203	4YBB_DA_PG4_3217	7O7Z_A2_SPM_1909	7O7Z_B5_SPM_4912	7O7Z_B5_SPM_4915	4U24_BA_DOL_3001	4U24_DA_DOL_3001	6DDD_1_G6V_3001	6YWY_A_SPM_3645	5J8A_AA_PG4_1670	5J8A_BA_PG4_1642	5J8A_DA_1PE_3185	5J8A_DA_PG4_3193	5J8A_DA_1PE_3202	5J8A_DA_PG4_3216	5J91_AA_PG4_1670	5J91_AA_T1C_1677	5J91_BA_PG4_1642	5J91_DA_1PE_3185	5J91_DA_PG4_3193	5J91_DA_1PE_3202	5J91_DA_PG4_3215	7DUI_A_HKO_1601	2TOB_A_TOA_100	2TOB_A_TOC_102	2TOB_A_2TB_101	5UYP_W_FME_101	5C45_X_51B_105	6VUI_A_PRF_101	6TFE_A_N6E_117	1F1T_A_ROS_101	7OAW_A_V6T_104	7OAW_B_GTP_101	7OAW_B_V6T_104	7OAW_C_SPM_101	7OAW_C_GTP_102	7OAW_C_V6T_105	7OAW_D_GTP_103	7OAW_D_V6T_104	4FAQ_A_SPM_445	4FAQ_A_SPM_446	2OGM_0_G19_2881	5V3F_A_74G_104	5V3F_B_74G_104	1J8G_A_SPM_62	7N30_23_ATP_3001	2QEX_0_NEG_8823	1KD1_A_SPR_9001	3MUM_R_C2E_1	4IO9_X_1F2_2929	6MPI_A_PAR_1693	7N1P_23_ATP_3001	7N1P_23_ATP_3002	5KVJ_A_ARG_101	4Y4O_1B_ARG_230	4U4O_2_GET_2181	6PCT_I_O8V_3001	4U3M_1_ANM_4218	4U3M_5_ANM_4260	4V97_AA_PAR_7111	4V97_CA_PAR_1741	5M1J_A3_5CR_101	6E82_A_TFX_102	4U51_1_3KF_4212	4U51_5_3KF_4248	7K00_A_PAR_1601	7LNF_A_LCG_102	7LNF_B_LCG_105	2VQF_A_PAR_1601	1J5A_A_CTY_2881	4NYG_A_VIB_101	4K31_B_AM2_101	4K31_B_AM2_102	4K31_C_AM2_101	4K31_C_AM2_102	7B5K_A_ERY_3237	7B5K_a_SY5_1714	7B5K_a_SY5_1715	7DUG_A_HJR_1601	3C44_A_PAR_24	3C44_B_PAR_24	4L47_QA_PAR_1667	4L47_XA_PAR_1673	1O15_A_TEP_34	6CAS_A_EUS_1814	2G5K_A_AM2_102	2G5K_B_AM2_101	7KVV_D_747_302	3SKW_A_GNG_120	3SKW_B_GNG_120	5DM7_X_HGR_6178	5DOY_1A_HGR_3915	5DOY_2A_HGR_3652	2H0W_B_MES_601	2H0W_B_MES_602	4QKA_A_2BA_201	4QKA_A_2BA_202	5NDJ_13_8UZ_2201	5NDJ_13_8UZ_2202	5NDJ_1G_8UZ_2201	5NDJ_1G_8UZ_2202	5NDJ_1H_8UZ_3002	5NDJ_1H_8UZ_3003	5NDJ_1H_8UZ_3004	5NDJ_1H_8UZ_3005	5NDJ_14_8UZ_3003	5NDJ_14_8UZ_3004	5NDJ_14_8UZ_3005	6WQN_1_ZC0_3001	4FB0_A_SPM_445	4TUA_QA_PAR_1696	4TUA_Z5_PPU_101	4TUA_XA_PAR_1715	4TUA_Z6_PPU_101	4V7Y_BA_ZIT_3351	4V7Y_DA_ZIT_3311	6DN1_Z_GZ7_201	7EAF_A_SAM_101	2F4V_A_D2C_1636	2F4V_A_AB9_1637	3F2X_X_FMN_200	6E1W_A_HNG_101	4QLM_A_2BA_203	4QLM_A_2BA_204	1UUD_B_P14_1046	6DLQ_A_PRP_201	3FO4_A_6GU_91	1K01_A_CLM_2884	4LFB_A_NMY_1822	4LFB_A_NMY_1823	4V57_AA_NMY_1601	4V57_AA_SCM_1662	4V57_CA_NMY_1601	4V57_CA_SCM_1661	1K73_A_ANM_9000	6C65_A_EKJ_101	6C65_B_EKJ_101	6C65_C_EKJ_101	3GES_A_6GO_91	6N5O_A_2BA_201	6N5O_A_2BA_202	4X64_A_PAR_1601	4X64_A_PAR_1602	4X64_A_PAR_1603	4X64_A_PAR_1604	4X64_A_PAR_1605	4X64_A_PAR_1606	1XNR_A_PAR_1545	6OFX_5_FME_101	3DIR_A_IEL_175	7MSZ_y_FME_101	4V7W_BA_CLM_3370	4V7W_DA_CLM_3334	4P70_QA_PAR_1601	4P70_XA_PAR_1601	3F2Q_X_FMN_200	7EOP_A_GTP_101	7EOP_A_J93_107	6TF3_A_3AT_109	6CC3_A_GTP_217	6CC3_B_GTP_211	4IOA_X_1F3_2931	6GZR_A_FH8_101	4KHP_A_PAR_1601	4KHP_A_PAR_1602	4KHP_A_PAR_1603	4KHP_A_PAR_1604	4KHP_A_PAR_1605	4KHP_A_PAR_1606	4KHP_A_PAR_1607	4KHP_A_PCY_1608	7EOK_A_GTP_101	7EOK_A_J8L_102	7NBU_V_FME_101	6XA1_L5_MVM_5246	6XJW_A_97C_101	6XJW_B_97C_101	6OLI_t_MVM_5110	5TCU_A_PAR_1601	7OF6_A_GTP_3386	7OF6_A_GTP_3387	7PJV_a_AM2_1652	7PJV_a_AM2_1657	4WSD_13_PAR_1749	4WSD_1G_PAR_1697	6CFJ_1A_EZG_4030	6CFJ_2A_EZG_3746	7RQ9_1A_6IF_4089	7RQ9_2A_6IF_3857	6N5S_A_2BA_202	6N5S_A_2BA_203	4PDQ_B_NMZ_101	7ELR_A_GTP_101	7ELR_B_GTP_101	6BSJ_R_TAM_101	5FKD_A_SAM_1095	6CHR_A_SPM_741	6N5T_A_2BA_201	6N5T_A_2BA_202	4LVV_A_FFO_101	4DR7_A_SRY_1928	6WD6_5_FME_101	7K51_1_FME_3001	4V9S_AX_FME_101	4V9S_CX_FME_101	7EOL_A_GTP_101	7EOL_A_J8O_107	2O3V_A_N33_50	6JBF_B_V71_100	3B4B_A_GLP_201	3B4B_A_3AD_-1	7OA3_A_V5Z_101	7OA3_A_GTP_102	7OA3_B_V5Z_101	7OA3_B_GTP_102	4LVX_A_H4B_101	4LVX_A_H4B_102	6OJ2_QA_PAR_1667	6HHQ_1_G5B_4224	6HHQ_AR_G5B_4264	2Z75_A_GLP_201	6CAO_A_PAR_1601	6CAO_A_PAR_1602	6CAO_A_PAR_1603	6CAO_A_PAR_1604	6CAO_A_PAR_1605	6CAO_A_PAR_1606	3SKL_A_GNG_120	3SKL_B_GNG_120	5V1L_B_SPM_303	2O3X_B_N30_1	6WD8_5_FME_101	6BU8_W_FME_101	4LT8_QA_PAR_1670	4LT8_XA_PAR_1675	3I56_0_TAO_2924	6OM0_t_MVM_5110	1YHQ_0_ZIT_9500	5EL6_13_PAR_1730	5EL6_1G_PAR_1681	5VCF_A_8OS_101	5BTP_B_AMZ_108	5BTP_A_AMZ_106	1O9M_B_BDG_2499	4W90_C_2BA_201	4W90_C_2BA_202	3DIG_X_SLZ_175	4KQY_A_SAM_201	6OLG_A2_MVM_5327	6OM7_t_MVM_5112	7NHM_D_FME_102	2MXS_A_PAR_101	6DTD_C_PG4_102	6S0X_A_ERY_3001	7P7Q_a_SCM_1652	5NDV_1_PAR_3401	5NDV_1_PAR_3402	5NDV_1_PAR_3403	5NDV_1_PAR_3404	5NDV_1_PAR_3405	5NDV_1_PAR_3406	5NDV_1_PAR_3409	5NDV_1_PAR_3410	5NDV_1_PAR_3411	5NDV_1_PAR_3412	5NDV_1_PAR_3413	5NDV_1_PAR_3414	5NDV_1_PAR_3415	5NDV_1_PAR_3416	5NDV_1_PAR_3417	5NDV_1_PAR_3418	5NDV_1_PAR_3419	5NDV_1_PAR_3420	5NDV_1_PAR_3421	5NDV_1_PAR_3423	5NDV_1_PAR_3424	5NDV_1_PAR_3425	5NDV_1_PAR_3426	5NDV_1_PAR_3427	5NDV_1_PAR_3428	5NDV_1_PAR_3429	5NDV_1_PAR_3430	5NDV_1_PAR_3431	5NDV_1_PAR_3433	5NDV_1_PAR_3434	5NDV_1_PAR_3435	5NDV_1_PAR_3437	5NDV_3_PAR_201	5NDV_3_PAR_202	5NDV_3_PAR_203	5NDV_4_PAR_201	5NDV_4_PAR_202	5NDV_2_PAR_1901	5NDV_2_PAR_1902	5NDV_2_PAR_1904	5NDV_2_PAR_1905	5NDV_5_PAR_3401	5NDV_5_PAR_3402	5NDV_5_PAR_3403	5NDV_5_PAR_3404	5NDV_5_PAR_3405	5NDV_5_PAR_3406	5NDV_5_PAR_3407	5NDV_5_PAR_3408	5NDV_5_PAR_3409	5NDV_5_PAR_3410	5NDV_5_PAR_3411	5NDV_5_PAR_3412	5NDV_5_PAR_3414	5NDV_5_PAR_3415	5NDV_5_PAR_3416	5NDV_5_PAR_3417	5NDV_5_PAR_3418	5NDV_5_PAR_3419	5NDV_5_PAR_3420	5NDV_5_PAR_3421	5NDV_5_PAR_3424	5NDV_5_PAR_3427	5NDV_5_PAR_3428	5NDV_7_PAR_201	5NDV_7_PAR_202	5NDV_8_PAR_201	5NDV_6_PAR_1901	5NDV_6_PAR_1902	5NDV_6_PAR_1903	5NDV_6_PAR_1905	5NDV_6_PAR_1906	7LNG_A_LCG_102	7LNG_B_LCG_104	1FMN_A_FMN_36	4ZNP_A_AMZ_101	4ZNP_B_AMZ_101	5ON6_1_HN8_4223	5ON6_AR_HN8_4263	1SM1_0_DOL_2882	5JU8_BA_ERY_9000	6YWV_A_SPM_3644	6LAZ_A_E7X_102	6LAZ_B_E7X_101	1KOD_B_CIR_1	3TZR_A_SS0_75	6BFB_X_DKM_500	5VJ9_A_SPM_102	5VJ9_B_SPM_103	5VJ9_B_SPM_104	5VJ9_C_SPM_102	5VJ9_D_SPM_102	4NYA_A_2QB_110	4NYA_B_2QB_107	1KOC_B_ARG_1	4JI3_A_SRY_1601	4V6Y_BA_FME_3001	6I0Y_A_TRP_3001	6E84_A_J0D_102	7OAX_A_V5Z_102	7OAX_A_SPM_103	7OAX_B_GTP_101	7OAX_B_SPM_102	7OAX_B_V5Z_103	7OAX_C_GTP_101	7OAX_C_SPM_102	7OAX_C_V5Z_103	7OAX_D_GTP_101	7OAX_D_SPM_102	7OAX_D_V5Z_103	4B5R_A_SAM_1095	6T3K_A_SPM_449	6T3K_A_SPM_450	6WTR_A_2BA_201	6WTR_A_2BA_202	1YIJ_0_TEL_9000	6QUL_1_FME_101	6QUL_A_JJH_3370	6P2H_A_GNG_101	1KQS_4_PPU_76	6LAS_A_SAM_101	6LAS_B_SAM_101	4V8F_BA_PAR_1715	4V8F_CA_PAR_1722	5UYQ_W_FME_101	2ET3_A_LLL_50	2ET3_B_LLL_51	7OAV_A_V5Z_101	7OAV_A_GTP_102	7OAV_B_V5Z_101	7OAV_B_GTP_102	7OAV_C_V5Z_101	7OAV_C_GTP_102	7OAV_D_V5Z_101	4V5G_AA_PAR_1601	4V5G_CA_PAR_1601	6GAW_BA_5GP_3203	6GAW_BA_5GP_3204	6GAW_BA_SPM_3205	6GAW_AA_SPM_3001	4U50_1_3L2_4212	4U50_5_3L2_4246	6MPF_A_PAR_1601	4AOB_A_SAM_1116	2ET4_A_NMY_50	2ET4_B_NMY_51	4U4N_2_EDE_2180	4U4N_6_EDE_2202	4FAW_A_SPM_452	6JJI_B_POH_104	4QK8_A_2BA_201	4QK8_A_2BA_202	4E8P_A_SPM_446	5IT8_AA_PG4_1670	5IT8_BA_PG4_1642	5IT8_DA_PG4_3191	5IT8_DA_1PE_3200	5IT8_DA_PG4_3213	5HL7_X_62B_3003	7N31_23_ATP_3001	5NRG_X_95H_3001	4LF5_A_HYG_1717	3G96_F_6MN_12	7LH5_AA_EDS_1805	4WT8_Ab_PAR_1601	4WT8_Bb_PAR_1601	4WT8_C1_3V6_3001	4WT8_D1_3V6_3001	2NZ4_P_GLP_5001	2NZ4_F_GLP_5002	2NZ4_G_GLP_5003	2NZ4_H_GLP_5004	4GPY_A_6HS_101	4GPY_A_6HS_102	7DUH_A_HJO_1601	4E8K_A_SPM_445	4U25_BA_VIR_3001	4U25_DA_VIR_3001	5UYM_W_FME_101	6YWX_A_SPM_3651	5WF0_A_FME_3001	5VP2_1A_M2D_4118	5VP2_2A_M2D_3864	5IBB_13_SPE_1748	5IBB_1G_SPE_1733	5IBB_14_SPE_3445	5IBB_14_SPE_3446	5IBB_1J_SPE_208	5ZEJ_B_PAR_101	2KXM_A_RIO_101	5FK3_A_SAM_1095	5FJC_A_SAM_101	4YAZ_R_4BW_106	4YAZ_A_4BW_103	3BNR_C_PAR_24	7D7V_A_GTP_101	7D7V_A_NAD_110	5FK4_A_SAM_1094	6WDA_5_FME_101	4WFB_X_3LK_3001	7NWT_5_FME_104	3E5F_A_EEM_216	6WDF_7_PHE_101	6WDF_7_FME_102	7TDC_A_GMI_101	3GX6_A_SAM_301	5WNT_A_B6M_1858	3G6E_0_HMT_9101	6Y6X_L5_OCW_5315	6HIV_CA_SPM_738	7R81_A1_3HE_8001	4U4R_1_3H3_4216	4U4R_5_3H3_4251	4U4U_1_3KD_4218	4U4U_5_3KD_4254	7NSH_BA_5GP_3206	7NSH_BA_5GP_3207	7NSH_BA_SPM_3208	7D7X_A_ADP_110	4P20_A_AKN_101	4P20_B_AKN_101	7FHI_A_53D_101	7KGB_A_WDP_3201	3G8T_E_GLP_5001	3G8T_Q_GLP_5002	3G8T_R_GLP_5003	3G8T_H_GLP_5004	5UX3_B_8OS_101	6WDH_5_FME_101	6DMD_A_G4P_201	6DMD_B_G4P_201	2HO7_A_G6P_401	5DGV_C_SPS_3401	5DGV_D_SPS_3401	4GPW_A_6HS_101	4GPW_A_6HS_102	6SVS_A_GTP_106	6SVS_A_A23_107	6SVS_B_GTP_106	6SVS_B_A23_107	4R0D_A_SPM_701	4R0D_A_SPM_702	4V72_BA_FME_3001	3F4H_Y_RS3_200	1Q81_5_PPU_76	6CK5_A_PRP_217	6CK5_B_PRP_216	6G7Z_B_MES_201	6DMC_A_G4P_201	6DMC_B_G4P_201	2UU9_A_PAR_1601	2YDH_A_SAM_1100	4V75_BA_FME_3001	7M4X_a_YQM_1601	5MDV_5_FME_103	1Q7Y_5_PUY_78	5KX9_X_6YG_108	1JZX_A_CLY_2881	4Q9Q_R_2ZZ_103	7LV0_1_FME_3001	5LKS_L5_3HE_5101	6OM6_1_KKL_3301	3IQN_A_SAM_301	3D2X_A_D2X_85	3D2X_B_D2X_84	7PJY_a_AM2_1626	7PJY_a_AM2_1628	7PJY_a_AM2_1636	6OLF_t_MVM_5112	3B4C_A_GLP_201	3B4C_A_3AD_-1	6UET_A_SAM_301	3G4S_0_MUL_9101	4LVY_A_LYA_101	4LVY_A_LYA_102	1K8A_A_CAI_4000	3IRW_R_C2E_1	6HBT_A_FXQ_103	5EL7_13_PAR_1749	5EL7_1G_PAR_1691	2Z74_A_G6P_201	6WD9_5_FME_101	4X4N_B_5GP_102	2O3Y_A_SPM_51	6XJQ_A_V4J_101	6XJQ_B_V4J_101	7ELS_A_GTP_101	7ELS_B_GTP_101	3CPW_0_ZLD_9500	5FKE_A_SAM_1095	1NTB_A_SRY_25	5O60_2_PHE_1002	5NDW_1_8UZ_3886	5NDW_1_8UZ_3887	5NDW_1_8UZ_3888	5NDW_1_8UZ_3889	5NDW_1_8UZ_3891	5NDW_1_8UZ_3892	5NDW_1_8UZ_3893	5NDW_1_8UZ_3894	5NDW_1_8UZ_3895	5NDW_2_8UZ_2029	5NDW_2_8UZ_2030	5NDW_3_8UZ_214	5NDW_4_8UZ_220	5NDW_5_8UZ_3850	5NDW_5_8UZ_3851	5NDW_5_8UZ_3852	5NDW_5_8UZ_3853	5NDW_5_8UZ_3854	5NDW_5_8UZ_3855	5NDW_5_8UZ_3856	5NDW_5_8UZ_3857	5NDW_6_8UZ_2061	5NDW_7_8UZ_209	3DIO_X_1PE_280	1Q8N_A_MGR_39	4DR6_A_SRY_1956	6WD7_5_FME_101	5J88_AA_PG4_1670	5J88_BA_PG4_1642	5J88_DA_PG4_3193	5J88_DA_1PE_3203	5J88_DA_PG4_3216	7K50_5_FME_101	5Z71_B_GET_201	7EOM_A_GTP_101	7EOM_A_J8R_102	2O3W_B_PAR_101	2HOO_A_BFT_95	6JBG_B_S81_301	2UUA_A_PAR_1601	2CKY_A_TPP_1084	2CKY_B_TPP_1082	1XMQ_A_PAR_1545	4P95_A_MES_601	1BYJ_A_GE3_30	5HKV_X_3QB_3001	7EOJ_A_J8F_101	5BJO_Y_747_104	5VCI_A_8OS_101	6UP0_C_YO3_104	6UP0_D_YO3_104	4B3M_A_ON0_2759	6QIQ_A_J48_101	6QIQ_B_J48_101	4V9R_AX_FME_101	4V9R_CX_FME_101	1FUF_B_SPM_98	3D2V_A_PYI_84	3D2V_B_PYI_82	6GYV_A_MES_201	5AFI_v_FME_105	6CFL_1A_EZM_4035	6CFL_1B_ARG_232	6CFL_2A_EZM_3691	6WD0_5_FME_101	6C63_A_EKJ_101	6C63_B_EKJ_101	6C63_C_EKJ_101	5TGA_1_8AN_3403	5TGA_5_8AN_3403	5LYV_A_CCC_101	5LYV_B_CCC_101	2BE0_A_JS5_50	2BE0_B_JS5_51	4X62_A_PAR_1601	4X62_A_PAR_1602	4X62_A_PAR_1603	4X62_A_PAR_1604	4X62_A_PAR_1605	4X62_A_PAR_1606	7RQ8_1A_6IF_4109	7RQ8_2A_6IF_3731	6CFK_1A_EZP_3987	6CFK_1B_ARG_228	6CFK_2A_EZP_3709	6AZ3_1_PAR_1801	6AZ3_1_PAR_1802	6AZ3_1_PAR_1803	6AZ3_1_PAR_1804	6AZ3_1_PAR_1805	6AZ3_2_PAR_1602	6AZ3_2_PAR_1603	6AZ3_2_PAR_1604	6AZ3_2_PAR_1605	6AZ3_7_PAR_201	6TF2_A_ATP_109	2ESI_A_KAN_51	2ESI_A_KAN_50	2ESI_B_KAN_52	4TS2_Y_CCC_101	4TS2_Y_38E_104	4F8V_A_SIS_101	4F8V_B_SIS_101	7E9I_A_J0C_101	5BR8_A_PAR_1601	5BR8_A_PAR_1602	5BR8_A_PAR_1603	5BR8_A_PAR_1604	5BR8_A_PAR_1605	5BR8_A_PAR_1606	4NXN_A_SRY_1601	2JUK_A_G0B_23	6XZB_A2_DI0_3001	4LFC_A_TOY_1738	6AZ4_A_GP3_101	6C64_A_EKM_101	6C64_B_EKM_101	3GER_A_6GU_91	6N5N_A_2BA_201	6N5N_A_2BA_202	3F2W_X_FMN_200	4X65_A_PAR_1601	4X65_A_PAR_1602	4X65_A_PAR_1603	4X65_A_PAR_1604	4X65_A_PAR_1605	4X65_A_PAR_1606	1YI2_0_ERY_9000	4L81_A_SAM_101	4WWW_RA_EM1_3135	4V7V_BA_CLY_3135	6FZ0_A_SAM_104	6OD9_A_AMZ_102	6OD9_B_AMZ_102	2LWK_A_0EC_101	4GXY_A_B1Z_302	4V4H_AA_KSG_1601	4V4H_CA_KSG_1601	1NJI_A_CLM_9001	3IQR_A_SAM_301	3F2Y_X_FMN_200	5WFS_A_FME_3001	7NQL_BA_5GP_3211	7NQL_BA_5GP_3212	7NQL_BA_SPM_3213	7NQL_AA_SPM_3001	2L8H_A_ARG_1	2L8H_A_L8H_2	6ORD_QA_PAR_1821	6ORD_XA_PAR_1794	4P6F_QA_PAR_1667	4P6F_XA_PAR_1672	4V7X_BA_ERY_3364	4V7X_DA_ERY_3330	4V56_AA_SCM_1661	4V56_CA_SCM_1659	4DV1_A_SRY_1601	5J7L_AA_PG4_1670	5J7L_AA_TAC_1680	5J7L_BA_PG4_1642	5J7L_DA_1PE_3185	5J7L_DA_PG4_3193	5J7L_DA_1PE_3202	5J7L_DA_PG4_3216	4QVI_B_MES_2204	6CAR_A_SIS_1809	3Q50_A_PRF_34	1I97_A_TAC_2001	1I97_A_TAC_2003	1I97_A_TAC_2004	1I97_A_TAC_2005	1ARJ_N_ARG_1	5FKH_A_SAM_1095	3FWO_A_MT9_2881	6VA2_A_QSV_101	6Y0G_L5_3HE_5101	4WF9_X_TEL_3001	4V51_AA_PAR_1816	4V51_CA_PAR_1790	5DOX_1A_HGR_3749	5DOX_2A_HGR_3515	5JVH_X_6O1_2901	7MSM_y_FME_101	3CME_6_PHE_77	5NDK_13_8UZ_2201	5NDK_13_8UZ_2202	5NDK_1G_8UZ_2201	5NDK_1G_8UZ_2202	5KPY_A_4PQ_101	7EOG_A_GTP_101	7EOG_A_J8F_102	2KU0_A_ISI_39	3SKI_A_GNG_120	3SKI_B_GNG_120	4NFO_C_SPM_101	4Q9R_R_2ZY_102	5WFK_A_FME_3001	1N8R_A_VIR_9403	4W92_C_2BA_208	4W92_C_2BA_209	4W2H_AA_PCY_3191	4W2H_CA_PCY_3176	4JF2_A_PRF_101	3PIP_X_LC2_2881	3PIP_X_LMA_2882	4LEL_QA_PAR_1666	4LEL_XA_PAR_1671	7EOI_A_J8F_101	4YB1_R_4BW_102	6QIR_A_J48_101	6QIR_A_J48_102	6QIR_C_J48_101	6QIR_D_J48_101	2HOK_A_TPP_93	6RW5_A_NAD_1701	6RW5_A_SPM_1702	6GZK_A_FH8_101	7OF4_A_GTP_3387	7OF4_A_GTP_3388	2UXD_A_PAR_3001	3JQ4_A_LC2_2881	6N5Q_A_2BA_201	6N5Q_A_2BA_202	6E8T_D_HZG_101	6E8T_C_HZG_101	6E8T_B_HZG_101	6E8T_A_HZG_101	7ELP_A_GTP_101	7ELP_B_GTP_101	3Q3Z_V_C2E_1	3Q3Z_A_C2E_2	3DIL_A_1PE_250	3DIL_A_1PE_251	3DIL_A_1PE_252	6HAG_A_SAH_101	1NTA_A_SRY_26	5FKF_A_SAM_1095	6E8S_A_EKJ_101	6E8S_B_EKJ_101	6E8S_B_SPM_107	7DWH_X_SAM_102	7DWH_Y_SAM_102	6BSH_R_TAM_101	4DR2_A_PAR_1601	4DR2_A_PAR_1602	4DR2_A_PAR_1603	4DR2_A_PAR_1604	4DR2_A_PAR_1605	4DR2_A_PAR_1606	4DR2_A_PAR_1607	4DR2_A_PAR_1608	4DR2_A_PAR_1609	4DR2_A_PAR_1610	4DR2_A_PAR_1611	4DR2_A_PAR_1612	4DR2_A_PAR_1613	4DR2_A_PAR_1614	4DR2_A_PAR_1615	4DR2_A_PAR_1616	4DR2_A_PAR_1617	6WD3_5_FME_101	7K54_1_FME_3001	3GOG_A_6GU_91	6WD4_5_FME_101	4DR5_A_SRY_1860	7EON_A_GTP_101	7EON_A_J8U_102	2KX8_A_ARG_392	7K53_5_FME_101	7MSC_y_FME_101	1AKX_A_ARG_47	2UUB_A_PAR_1601	3V7E_C_SAM_913	3V7E_D_SAM_407	2HOL_A_TPP_105	6DLS_A_PRP_201	2UXC_A_PAR_2001	3G9C_E_GLP_5001	5BJP_Y_747_104	7OF3_A_GTP_3359	4B3R_A_M5Z_2733	3FO6_A_6GO_91	1VQ8_4_SPS_9701	7PJS_a_AM2_1684	7PJS_a_AM2_1685	7PJS_a_AM2_1689	5A9Z_BA_NMY_1601	1PBR_A_PA1_101	1PBR_A_CYY_102	4V9Q_AA_BLS_4001	4V9Q_CA_BLS_4405	6TNU_BQ_3HE_3402	3F2T_X_FMN_200	2L1V_A_PRF_37	4W2F_AA_UAM_3232	4W2F_CA_UAM_3202	4X66_A_PAR_1601	4X66_A_PAR_1602	4X66_A_PAR_1603	4X66_A_PAR_1604	4X66_A_PAR_1605	4X66_A_PAR_1606	3SD3_A_FFO_3631	3S4P_A_JS6_50	3S4P_B_JS6_51	6HC5_A_FXT_105	6DLT_A_PRP_207	6CC1_B_GTP_201	5VJB_A_SPM_102	5VJB_B_SPM_102	5VJB_C_SPM_102	5VJB_D_SPM_102	5LWJ_A_GTP_101	6TF1_A_ADP_109	1YLS_A_DAI_100	1YLS_C_DAI_100	5IB7_13_PAR_1741	5IB7_1G_PAR_1702	5IB7_1G_SPE_1703	5IB7_14_SPE_3436	5IB7_14_SPE_3437	4IOC_X_1F4_2929	4V7U_BA_ERY_3136	6XZA_A2_DI0_3001	2ESJ_A_LIV_50	2ESJ_B_LIV_51	6UC9_B_CMG_109	2HOP_A_218_92	4F8U_A_SIS_101	4F8U_B_SIS_101	3L3C_P_G6P_5001	3L3C_Q_G6P_5002	3L3C_G_G6P_5003	3L3C_H_G6P_5004	2GCV_A_MES_501	2GCV_B_MES_502	6CAQ_A_EUS_1809	6HD7_1_3HE_3401	6GB2_BA_5GP_3203	6GB2_BA_5GP_3204	6GB2_BA_SPM_3205	3SKR_A_GNG_120	3SKR_B_GNG_120	6WRU_1_U7Y_3001	2FD0_A_LIV_1001	2FD0_B_LIV_2001	4DV5_A_SRY_1601	6UC7_B_Q44_109	1N33_A_PAR_1545	1YRJ_A_AM2_151	1YRJ_B_AM2_150	7KVT_B_2ZY_101	4X4V_B_5GP_502	4X4V_D_5GP_101	1F27_A_BTN_33	4V52_AA_NMY_1601	4V52_CA_NMY_1601	4GKK_A_PAR_1785	2F4T_B_AB9_1	5KCS_1A_EVN_3001	7NQH_AA_SPM_3001	7NQH_BA_5GP_1791	7NQH_BA_5GP_1792	7NQH_BA_SPM_1793	5LZB_v_FME_101	6DN3_Y_GZ4_201	3D2G_A_TPP_83	3D2G_B_TPP_83	1YKV_A_DAI_100	1YKV_C_DAI_100	4V9C_AA_NMY_1657	4V9C_BA_NMY_3162	4V9C_BA_NMY_3163	4V9C_BA_NMY_3164	4V9C_BA_NMY_3165	4V9C_BA_NMY_3166	4V9C_BA_NMY_3167	4V9C_CA_NMY_1672	4V9C_DA_NMY_3185	4V9C_DA_NMY_3186	4V9C_DA_NMY_3187	4V9C_DA_NMY_3188	4V9C_DA_NMY_3189	4V9C_DA_NMY_3190	4TUC_Z5_PPU_101	4TUC_Z6_PPU_101	3CMA_6_PHE_77	1MWL_A_GET_45	1MWL_A_GET_46	4NYB_A_2QC_101	6PQ7_C_OXV_102	4V6Z_BA_FME_3001	6GAZ_AA_SPM_3001	4V55_AA_LLL_1661	4V55_CA_LLL_1662	7P7U_a_SCM_1660	4TUD_QA_PAR_1691	4TUD_Z5_PPU_101	4TUD_XA_PAR_1705	4TUD_Z6_PPU_101	4V5D_AA_PAR_1799	4V5D_CA_PAR_1800	6XHX_1A_ERY_4021	6XHX_1B_ARG_233	6XHX_2A_ERY_3734	5JC9_AA_PG4_1670	5JC9_BA_PG4_1642	5JC9_DA_1PE_3188	5JC9_DA_PG4_3196	5JC9_DA_1PE_3205	5JC9_DA_PG4_3218	4V5C_AA_PAR_1814	4V5C_CA_PAR_1817	6CZR_1A_FSD_3801	6CZR_1B_ARG_223	4U53_1_3J6_4213	4U53_5_3J6_4246	6I7V_BA_PG4_1607	3K1V_A_PRF_301	1FYP_A_PAR_28	3EGZ_B_CTC_601	2AU4_A_GTP_42	4LF8_A_PAR_1810	4LF8_A_PAR_1811	4LF8_A_PAR_1812	4LF8_A_PAR_1813	4LF8_A_PAR_1814	4LF8_A_PAR_1815	4LF8_A_PAR_1816	4LF8_A_PAR_1817	4LF8_A_PAR_1818	6XKO_A_PRF_201	2O45_A_RU6_2881	6DTI_A_PAR_1601	5V7Q_A_917_5001	5WE6_A_FME_3001	7A0R_X_QTZ_2901	2A04_A_NMY_17	2A04_A_NMY_18	2A04_C_NMY_1	2A04_C_NMY_17	4LF6_A_NMY_1832	4LF6_A_NMY_1833	4LF6_A_NMY_1834	4LF6_A_NMY_1835	4LF6_A_NMY_1836	7DUK_A_SIS_1835	7D12_A_L94_101	6YSI_1_T1C_3160	5JTE_BA_ERY_9000	4E8T_A_SPM_440	4E8T_A_SPM_441	6TFG_A_PPS_112	6XZ7_A_DI0_3175	4U26_BA_DOL_3001	4U26_DA_DOL_3001	7DUL_A_SIS_1835	3OVB_C_ATP_851	2OGO_0_G34_0	5GAK_1_3HE_3401	4WOI_BA_PAR_3002	4WOI_BA_PAR_3003	4WOI_BA_PAR_3004	4WOI_BA_PAR_3005	4WOI_CA_PAR_3166	4WOI_CA_PAR_3168	4WOI_CA_PAR_3169	4WOI_CA_PAR_3170	2BEE_A_JS4_50	2BEE_B_JS4_51	2N0J_A_RIO_101	3OW2_0_EMK_8163	1XBP_0_MUL_2881	3BNQ_C_PAR_101	1ET4_A_CNC_701	1ET4_B_CNC_801	1ET4_C_CNC_901	1ET4_D_CNC_1001	1ET4_E_CNC_601	3E5E_A_SAH_220	3GX5_A_SAM_301	6YL5_A_SAH_101	6YL5_B_SAH_101	6YL5_C_SAH_101	6YL5_E_SAH_101	6YL5_F_SAH_101	6YL5_G_SAH_101	6YL5_I_SAH_101	6YL5_I_SAH_102	6YL5_K_SAH_101	6WDE_7_PHE_101	5AA0_AA_8AN_3002	5AA0_BA_NMY_1601	3F4E_Y_FMN_200	3GX2_A_SFG_301	4V6O_BB_FME_3001	5ZEI_A_GET_101	5ZEI_B_GET_101	3IWN_A_C2E_501	3IWN_B_C2E_601	7M4U_a_YQM_1601	6WZR_A_UG1_106	6WZR_B_UG1_103	4V78_BA_FME_3001	6HA1_A_TEL_3001	1K9M_A_TYK_9000	3G71_0_WIN_9101	4U4Q_1_HMT_4217	4U4Q_5_HMT_4255	5J5B_AA_PG4_1670	5J5B_AA_TAC_1678	5J5B_BA_PG4_1601	5J5B_DA_1PE_3185	5J5B_DA_PG4_3193	5J5B_DA_1PE_3202	5J5B_DA_PG4_3215	6V9D_B_QW4_101	6V9D_B_QW4_102	6V9D_E_QW4_101	6WDB_5_FME_101	1LVJ_A_PMZ_47	6YML_A_AMP_101	6YML_A_DSH_102	6YML_C_DSH_101	7A3Y_A_BER_101	4WFA_X_ZLD_3001	4V76_BA_FME_3001	7MT7_y_FME_101	5OB3_A_1TU_101	5OB3_A_SPM_104	6WDL_1_FME_3001	6WDL_7_PHE_101	7EDL_A_GET_101	7EDL_B_GET_101	5WDT_A_FME_3001	6WDK_5_FME_101	6WDK_7_PHE_101	6HA8_A_TEL_3001	6YMK_A_MTA_101	6YMK_B_MTA_101	6YMK_C_MTA_101	6YMK_F_MTA_101	6YMK_G_MTA_101	6YMK_I_MTA_101	6YMK_M_MTA_101	6YMK_M_MTA_102	6YMK_O_MTA_101	5V0O_A_8OS_101	3MUT_R_C2E_1	7E9E_A_J0C_101	3TD1_B_GET_50	3TD1_B_GET_51	7KVU_G_2ZY_106	6I9R_A_H8T_3431	1UUI_B_P12_1046	1Q82_5_PPU_76	3SKT_A_GNG_89	3SKT_B_GNG_89	3CC4_0_ANM_2924	4GKJ_A_PAR_1785	2F4U_B_AB6_41	5LZC_v_FME_101	6DN2_Y_GZG_203	2M4Q_1_AM2_101	4QLN_A_2BA_201	4QLN_A_2BA_202	6E1T_A_MES_101	1AM0_A_AMP_41	4W29_BA_NMY_2904	4W29_CA_NMY_1601	5I4L_6_UAM_2134	5IB8_1G_SPE_1725	5IB8_14_SPE_3458	6VMY_A_B1Z_412	4DV3_A_SRY_1601	4V7Z_BA_TEL_3362	4V7Z_DA_TEL_3320	7RQC_1B_ARG_231	6CAP_A_SIS_1792	6WRS_1_U7V_3001	5MEI_1_7MB_4216	5MEI_AR_7MB_4239	4TUE_QA_PAR_1693	4TUE_Z5_PPU_101	4TUE_XA_PAR_1715	4TUE_Z6_PPU_101	6MKN_A_PAR_1601	2KTZ_A_ISH_39	1N32_A_PAR_1545	5LZD_v_FME_101	6Y69_A_OCW_3001	4V53_AA_LLL_2061	4V53_AA_LLL_2062	4V53_AA_LLL_2063	4V53_CA_LLL_2062	4V53_CA_LLL_2063	4V53_CA_LLL_2064	5KCR_1A_6UQ_3001	4V9B_CA_T1C_1800	4TUB_QA_PAR_1681	4TUB_Z5_PPU_101	4TUB_XA_PAR_1710	4TUB_Z6_PPU_101	3SLQ_A_5GP_120	3SLQ_B_5GP_120	3DIQ_A_HRG_175	3DIQ_A_1PE_280	6AZ1_1_PAR_2302	6AZ1_1_PAR_2303	6AZ1_1_PAR_2305	6AZ1_1_PAR_2306	6N5K_A_2BA_201	6N5K_A_2BA_202	1XPF_A_SPM_108	3FU2_A_PRF_101	3FU2_B_PRF_101	3FU2_C_PRF_101	6TF0_A_NAI_111	4TS0_Y_CCC_101	4TS0_Y_38E_107	6UC8_B_ANG_101	1RAW_A_AMP_37	6DLR_A_PRP_201	4B3T_A_3TS_2733	3SKZ_A_GMP_120	3SKZ_B_GMP_120	1XMO_A_PAR_1545	2H0Z_A_G6P_301	2GIS_A_SAM_301	4B3S_A_RPO_2800	4LFA_A_HYG_1716	4RZD_A_PRF_201	4JYA_A_PAR_1614	1XNQ_A_PAR_1545	2L94_A_L94_46	1J7T_A_PAR_45	1J7T_B_PAR_46	7ELQ_A_GTP_101	7ELQ_B_GTP_101	7MDZ_5_Z2V_5288	4V7S_BA_TEL_3135	3DIM_A_1PE_280	5FKG_A_SAM_1095	3SLM_A_DGP_120	3SLM_B_DGP_120	4V7T_BA_CLM_3136	6WD5_5_FME_101	3J5L_A_ERY_9000	5V8I_1B_ARG_1001	4DR4_A_PAR_1601	4DR4_A_PAR_1602	4DR4_A_PAR_1603	4DR4_A_PAR_1604	4DR4_A_PAR_1605	4DR4_A_PAR_1606	4DR4_A_PAR_1607	4DR4_A_PAR_1608	4DR4_A_PAR_1609	4DR4_A_PAR_1610	4DR4_A_PAR_1611	4DR4_A_PAR_1612	4DR4_A_PAR_1613	4DR4_A_PAR_1614	4DR4_A_PAR_1615	4DR4_A_PAR_1616	4DR4_A_PAR_1617	4DR4_A_PAR_1618	7K52_1_FME_3001	7EOO_A_GTP_101	7EOO_A_J8X_102	5JVG_X_6NO_2901	4Y1J_A_GTP_201	7L0Z_G_2ZY_101	7L0Z_G_SPM_102	7L0Z_G_SPM_103	7L0Z_G_SPM_104	2GDI_X_TPP_100	2GDI_Y_TPP_100	6QIT_A_J48_101	6QIT_A_J48_102	6QIT_C_J48_101	6QIT_D_J48_101	2HOM_A_TPS_97	2UUC_A_PAR_1601	7EOH_A_J8F_101	7OF2_A_GTP_3382	7OF2_A_GTP_3383	2UXB_A_PAR_3001	4Y1M_B_GTP_212	4Y1M_A_GTP_208	1NWY_0_ZIT_2881	7TD7_A_VIB_104	4YB0_R_GDP_101	4YB0_R_C2E_102	4YB0_A_GDP_101	4YB0_A_C2E_102	6YLB_A_SAM_101	6YLB_B_SAM_101	6YLB_C_SAM_101	6YLB_F_SAM_101	6YLB_G_SAM_101	6YLB_I_SAM_101	6YLB_M_SAM_101	6YLB_N_SAM_101	6YLB_O_SAM_101	7OF5_A_GTP_3370	6RW4_A_NAD_1701	6RW4_A_SPM_1702	6QIS_A_J48_101	6QIS_B_J48_101	6QIS_C_J48_101	6QIS_C_J48_102	6QIS_E_J48_101	6QIS_E_J48_102	6QIS_G_J48_101	6QIS_H_J48_101	4ZC7_A_PAR_101	4ZC7_C_PAR_101	2HOJ_A_TPP_114	1VQ9_4_SPS_9701	5NDG_2_GET_2012	5NDG_2_GET_2013	5NDG_2_GET_2014	5NDG_1_GET_3808	5NDG_1_GET_3810	5NDG_1_GET_3811	5NDG_1_GET_3812	5NDG_6_GET_2013	5NDG_6_GET_2014	5NDG_6_GET_2015	5NDG_5_GET_3844	5NDG_5_GET_3845	5NDG_5_GET_3846	5NDG_5_GET_3848	5NDG_5_GET_3850	5NDG_5_GET_3851	4Z3S_1A_4M2_3894	6XB7_A_UYS_101	4W2G_CA_PCY_3178	6WOO_3_U6A_101	5Z1H_A_FSJ_301	6E8U_B_HZD_106	6N5P_A_2BA_201	6N5P_A_2BA_202	4XW7_A_AMZ_101	6WD2_5_FME_101	4WF1_CA_NEG_1657	6TB7_A_AMP_101	4DR3_A_SRY_1601	7K55_1_FME_3001	7OIZ_A_PAR_1601	2KGP_A_MIX_26	3SUX_X_THF_103	2QWY_A_SAM_100	2QWY_B_SAM_300	2QWY_C_SAM_500	6WQQ_1_RD8_3001	6VA4_B_QSY_101	5OBM_1_LLL_3989	5OBM_1_LLL_3990	5OBM_1_LLL_3991	5OBM_1_LLL_3992	5OBM_1_LLL_3993	5OBM_1_LLL_3994	5OBM_1_LLL_3995	5OBM_1_LLL_3996	5OBM_1_LLL_3997	5OBM_1_LLL_3998	5OBM_1_LLL_3999	5OBM_1_LLL_4000	5OBM_1_LLL_4001	5OBM_1_LLL_4002	5OBM_1_LLL_4003	5OBM_1_LLL_4004	5OBM_3_LLL_220	5OBM_4_LLL_224	5OBM_2_LLL_2043	5OBM_2_LLL_2044	5OBM_2_LLL_2045	5OBM_5_LLL_4151	5OBM_5_LLL_4152	5OBM_5_LLL_4153	5OBM_5_LLL_4154	5OBM_5_LLL_4155	5OBM_5_LLL_4156	5OBM_5_LLL_4157	5OBM_5_LLL_4158	5OBM_5_LLL_4159	5OBM_5_LLL_4160	5OBM_5_LLL_4161	5OBM_5_LLL_4162	5OBM_5_LLL_4163	5OBM_5_LLL_4164	5OBM_5_LLL_4165	5OBM_5_LLL_4166	5OBM_5_LLL_4167	5OBM_5_LLL_4168	5OBM_5_LLL_4169	5OBM_5_LLL_4170	5OBM_5_LLL_4171	5OBM_5_LLL_4172	5OBM_5_LLL_4173	5OBM_5_LLL_4174	5OBM_5_LLL_4175	5OBM_5_LLL_4176	5OBM_5_LLL_4177	5OBM_7_LLL_232	5OBM_7_LLL_233	5OBM_8_LLL_221	5OBM_8_LLL_222	5OBM_6_LLL_2164	5OBM_6_LLL_2165	5OBM_6_LLL_2166	5OBM_6_LLL_2167	5OBM_6_LLL_2169	5OBM_6_LLL_2170	5OBM_6_LLL_2171	5OBM_6_LLL_2172	5OBM_6_LLL_2173	5OBM_6_LLL_2176	2HHH_A_KSG_1523	6IZP_A_B2R_101	6IZP_A_B2R_102	6V39_AN1_FME_3001	3K0J_E_TPP_601	3K0J_F_TPP_602	3F30_X_FMN_200	6VA3_A_MQC_101	3B4A_A_GLP_401	7D7Z_A_GTP_101	7D7Z_A_NAD_129	6T3R_A_SPM_452	6T3R_A_SPM_453	4V7A_BA_FME_3001	7EDM_B_GET_101	7EDM_B_GET_102	7NSJ_AA_SPM_3001	7NSJ_BA_5GP_1791	7NSJ_BA_SPM_1792	6WDJ_5_FME_101	6V9B_B_QSA_101	6V9B_B_QSA_102	6V9B_D_QSA_101	2OE5_B_AM2_101	4LX5_A_29G_501	4V70_BA_FME_3001	6YMJ_A_CBV_101	6YMJ_A_ADN_102	6YMJ_A_ADN_103	6YMJ_C_CBV_101	6YMJ_C_ADN_102	6YMJ_F_CBV_101	6YMJ_F_ADN_102	6YMJ_F_ADN_103	6YMJ_I_CBV_101	6YMJ_I_ADN_102	6YMJ_M_CBV_101	6YMJ_M_ADN_102	6YMJ_N_ADN_101	6YMJ_O_CBV_101	6YMJ_O_ADN_102	7N2V_16_SCM_1601	7N2V_16_SCM_1602	7N2V_23_ATP_3002	1ZZ5_A_CNY_42	1ZZ5_A_CNY_43	1ZZ5_C_CNY_41	1ZZ5_C_CNY_44	2MIY_A_PRF_101	4W2I_AA_NEG_3216	4W2I_AA_NEG_3217	4W2I_AA_NEG_3218	4W2I_AA_NEG_3219	4W2I_AW_NEG_3004	4W2I_CA_NEG_3170	4W2I_CA_NEG_3171	4W2I_CA_NEG_3172	4W2I_CA_NEG_3173	4W2I_CW_NEG_3002	1UTS_B_P13_1046	5WIT_1A_AQJ_3969	5WIT_2A_AQJ_3677	1EI2_A_NMY_26	1VVJ_QA_PAR_1661	1VVJ_XA_PAR_1664	5TGM_1_PHE_3401	5TGM_5_PHE_3401	5TGM_P_SPS_101	5TGM_P_8AN_102	7D82_A_NAD_108	1YIT_0_VIR_9000	3J7Z_A_ERY_9000	4V77_BA_FME_3001	5V9Z_A_8OS_101	6YMM_A_SAM_101	6YMM_B_SAM_201	6YMM_C_SAM_101	4U6F_1_ZBA_4206	4U6F_5_ZBA_4256	1HNZ_A_HYG_1632	3MUR_R_C2E_1	1DDY_A_B12_101	1DDY_C_B12_301	1DDY_E_B12_501	1DDY_G_B12_701	1NBK_A_GND_35	1NBK_A_GND_36	6B4V_B_BLS_9001	6BOH_B_BLS_9001	7RQB_1B_ARG_231	7REX_A_PRF_101	7REX_A_PRF_102	7REX_B_PRF_101	7REX_B_PRF_102	7REX_C_PRF_101	7REX_C_PRF_102	3DS7_A_GNG_120	3DS7_B_GNG_320	4U3U_1_3HE_4215	4U3U_5_3HE_4252	1JZZ_A_ROX_2881	6WTL_A_2BA_201	6WTL_A_2BA_202	3E5C_A_SAM_216	4V5Y_AA_PAR_1661	4V5Y_CA_PAR_1662	6WDM_7_PHE_101	6WDM_7_FME_102	7RQE_1A_CLM_4017	7RQE_1B_ARG_231	7RQE_2A_CLM_3747	3GX3_A_SAH_301	4WFN_X_ERY_2902	1TOB_A_TOA_28	1TOB_A_TOC_30	4V79_BA_FME_3001	1TN2_A_SPM_77	3GCA_A_PQ0_34	2YIE_Z_FMN_1114	6WZS_B_UG4_107	6WZS_A_UG4_107	5WIS_1A_MT9_4113	5WIS_2A_MT9_3897	4XWF_A_AMZ_101	4L71_QA_PAR_1666	4L71_XA_PAR_1673	2FCY_A_NMY_1001	2FCY_B_NMY_2001	5FK1_A_SAM_1095	5MDZ_5_FME_101	6Q57_A_T0A_101	6Q57_A_T0A_102	7SSO_1_FME_3001	6WDC_5_FME_101	5FK6_A_SAM_1095	7A18_X_MIV_2901	1I9V_A_NMY_200	6WDD_5_FME_101	6WDD_7_PHE_101	7TDA_A_TPP_201	4E8N_A_SPM_446	5WNV_A_B6M_1856	4V6N_AB_FME_3001	5TBW_1_7AL_4210	5TBW_AR_7AL_4246	3NPN_A_SAH_55	6OPE_QA_PAR_1663	6OPE_XA_PAR_1670	6OF6_QA_PAR_1711	6OF6_XA_PAR_1717	6OF1_1A_DI0_4098	6OF1_2A_DI0_3846	7MD7_1A_YXM_4055	7MD7_1B_ARG_228	7MD7_2A_YXM_3758	6ND5_1A_CLM_4102	6ND5_2A_CLM_3888	7O7Y_A2_SPM_1909	4KZD_R_1TU_103	7FJ0_A_53D_101	6TFF_A_NAD_109	5D5L_A_PRF_117	5D5L_B_PRF_109	5D5L_C_PRF_104	5D5L_D_PRF_106	4FAR_A_SPM_452	4FAR_A_SPM_453	2OGN_0_G80_2881	2O43_A_ERN_2881	1LC4_A_TOY_47	1LC4_B_TOY_48	4WRA_13_PAR_1745	4WRA_1G_PAR_1686	4FAU_A_SPM_425	2O44_A_JOS_2881	6XKN_A_PRF_201	4U20_BA_VIF_3001	4U20_DA_VIF_3001	3RKF_A_DX4_91	3RKF_B_DX4_91	3RKF_C_DX4_91	3RKF_D_DX4_91	3T1H_A_PAR_1783	4V8J_AA_PAR_1694	4V8J_CA_PAR_1695	4V5L_AA_PAR_1601	1QD3_A_BDG_46	1QD3_A_CYY_47	7N2C_23_ATP_3001	7A0S_X_QU2_2901	1M90_5_SPS_9080	4JI8_A_SRY_1601	7DUJ_A_SIS_1833	4LF7_A_PAR_1810	4LF7_A_PAR_1811	4LF7_A_PAR_1812	4LF7_A_PAR_1813	4LF7_A_PAR_1814	4LF7_A_PAR_1815	4LF7_A_PAR_1816	4LF7_A_PAR_1817	4LF7_A_PAR_1818	6DDG_1_G6M_3001	6E81_A_TFX_101	5DGF_1_SPS_3401	7LNE_A_LCG_102	7LNE_B_LCG_104	4U27_BA_VIF_3001	4U27_DA_VIF_3001	5XI1_S_MYC_101	5XI1_S_MYC_102	3MXH_R_C2E_1	4LNT_QA_PAR_1666	4LNT_XA_PAR_1673	3DLL_X_ZLD_2911	7P7S_a_SCM_1675	6LAX_A_SAM_101	6LAX_B_SAM_101	2VQE_A_PAR_1854	4LF9_A_LLL_1743	4K32_A_GET_101	4K32_B_GET_101	4V8C_CA_PAR_1841	4V8C_DA_PAR_1805	6TFH_A_NAD_110	1FJG_A_PAR_1545	1FJG_A_SCM_1633	1FJG_A_SRY_1634	4JI1_A_SRY_1601	6YWS_A_SPM_3661	7NSQ_A_TEL_9000	2YGH_A_SAM_1096	7P7T_a_SCM_1615	4AQY_A_AM2_3001	4AQY_A_AM2_3002	4AQY_A_AM2_3003	4AQY_A_AM2_3004	4AQY_A_AM2_3005	2TRA_A_SPM_76	6XHY_1A_TEL_4076	6XHY_2A_TEL_3845	4U52_1_3J2_4209	4U52_5_3J2_4254"
columns = s.split()
df = pd.read_csv("data/rmscore_normalized_by_average_length_complete_dataset.csv", header=None)
df.columns = columns
raw_val = df.values
indices = {name: idx for (idx, name) in enumerate(columns)}

sam_cols = [name for name in columns if 'SAM' in name]
sam_idx = [indices[name] for name in sam_cols]
sam_pairwise = raw_val[sam_idx, :][:, sam_idx]

copies = ['4OQU_A_SAM_101', '5FK5_A_SAM_1095', '7DWH_X_SAM_102', '6UET_A_SAM_301', '6FZ0_A_SAM_104', '2QWY_A_SAM_100',
          '2QWY_B_SAM_300', '2QWY_C_SAM_500', '6YMM_B_SAM_201']
copies_idx = [indices[name] for name in copies]
copies_pairwise = raw_val[copies_idx, :][:, copies_idx]
# print(copies_pairwise)

'''
def pick_similar(name, sim_thresh=0.75):
    """
    returns all indices in the original df that match this name
    """
    train_id = indices[name]
    similarities = raw_val[train_id, :]
    # plt.hist(similarities)
    # plt.show()
    similar_ones = np.where(similarities > sim_thresh)[0]
    # print(sorted({columns[idx]: similarities[idx] for idx in similar_ones}))
    return similar_ones


# pick_similar(sam_cols[0])

# Now for those columns, group together systems
columns_copy = columns.copy()
already_picked = np.zeros(len(columns_copy))
groups = {}
# To keep track of id:cluster_id and cluster_id:name
labels = np.zeros(len(columns_copy))
label_value_to_rep = {}
for i, name in enumerate(columns_copy):
    # If we already included this name in a group, skip
    if already_picked[i]:
        continue

    # Pick a new group, and subset to pick only systems that were not selected before
    group = pick_similar(name)
    to_select = np.zeros(len(columns_copy))
    to_select[group] = 1
    subset_group = np.logical_and(1 - already_picked, to_select)
    subset_group = np.where(subset_group)[0]
    already_picked[subset_group] = True

    # keep an id:cluster mapping
    labels[subset_group] = len(groups)
    label_value_to_rep[len(groups)] = name
    cluster_names = [columns[idx] for idx in subset_group]
    groups[name] = cluster_names
'''

# '''
# %%%%%%% ALTERNATIVE
print("Clustering")
from sklearn.cluster import AgglomerativeClustering

clustering = AgglomerativeClustering(metric='precomputed',
                                     n_clusters=None,
                                     compute_full_tree=True,
                                     linkage='single',
                                     distance_threshold=0.25).fit(1 - raw_val)
labels = clustering.labels_
unique_values = np.unique(labels)
groups = {}
# This reverse map (cluster id : systems) is useful to remove robin systems
label_value_to_rep = {}
for value in unique_values:
    cluster = np.where(labels == value)[0]
    cluster_names = [columns[idx] for idx in cluster]
    group_rep = cluster_names[0]
    groups[group_rep] = cluster_names
    label_value_to_rep[value] = group_rep
# '''

different_ligs = 0
for name, group in groups.items():
    ligands = [s.split('_')[2] for s in group]
    if len(np.unique(ligands)) > 1:
        print(name, len(np.unique(ligands)), len(ligands), ligands)
    different_ligs += len(np.unique(ligands))
    # print(name, len(group))
    # if 'SAM' in name:
    #     print(group)
# plt.hist([len(group) for group in groups.values()])
# plt.show()
# print(groups)
print("Different", different_ligs, len(groups))

# Handle robin systems:
robin_pdb_names = ["2GDI", "5BTP", "2QWY", "3FU2"]
robin_groups = {}
for name in robin_pdb_names:
    robin_ids = [indices[column] for column in columns if column.startswith(name)]
    robin_clusters = labels[robin_ids]
    assert len(np.unique(robin_clusters)) == 1
    robin_cluster = robin_clusters[0]
    robin_rep = label_value_to_rep[robin_cluster]
    robin_groups[robin_rep] = groups.pop(robin_rep)

# Split based on keys + add ROBIN
train_cut = int(0.85 * len(groups))
train_groups_keys = list(groups.keys())[:train_cut]
test_groups_keys = list(groups.keys())[train_cut:]
train_groups = {key: groups[key] for key in train_groups_keys}
test_groups = {key: groups[key] for key in test_groups_keys}
test_groups.update(robin_groups)
print("Number of groups", len(train_groups), len(test_groups))

train_names_grouped = list(train_groups.keys())
test_names_grouped = list(test_groups.keys())
train_names = set(chain.from_iterable([[name for name in group] for group in train_groups.values()]))
test_names = set(chain.from_iterable([[name for name in group] for group in test_groups.values()]))
print("Number of examples", len(train_names), len(test_names))


# print(sorted(train_names))
# print()
# print(sorted(test_names))

def compute_max_train_test(train_names, test_names):
    train_ids = [indices[name] for name in train_names]
    test_ids = [indices[name] for name in test_names]
    pairwise = raw_val[train_ids, :][:, test_ids]
    max_test = np.max(pairwise, axis=1)
    print(max_test.mean(), max_test.std())
    return max_test


# current_data = pd.read_csv("data/rnamigos2_dataset_consolidated.csv")[["PDB_ID_POCKET", "TYPE"]]
# current_data = current_data.drop_duplicates()
# train, test = set(), set()
# for pocket_name, split in current_data.values:
#     if split == 'TEST':
#         test.add(pocket_name)
#     else:
#         train.add(pocket_name)
# pickle.dump((train, test), open("temp_train_test.p", 'wb'))
# train, test = pickle.load(open("temp_train_test.p", 'rb'))
# max_test_previous = compute_max_train_test(train, test)
# plt.hist(max_test_previous, alpha=0.5, bins=20)

# max_test_new = compute_max_train_test(train_names, test_names)
# plt.hist(max_test_new, alpha=0.5, bins=20)
# max_test_new = compute_max_train_test(train_names_grouped, test_names_grouped)
# plt.hist(max_test_new, alpha=0.5, bins=20)
# plt.show()

pickle.dump((train_names, test_names, train_names_grouped, test_names_grouped), open("data/train_test_75.p", 'wb'))